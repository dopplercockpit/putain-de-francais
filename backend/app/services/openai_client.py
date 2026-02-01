import json
from typing import Any, Dict, List, Optional

from openai import OpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_TEXT_MODEL

_client: Optional[OpenAI] = None


def get_openai_client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _build_input(system_prompt: Optional[str], user_prompt: str) -> List[Dict[str, str]]:
    if system_prompt:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    return [{"role": "user", "content": user_prompt}]


def _response_text(resp: Any) -> str:
    if hasattr(resp, "output_text") and resp.output_text:
        return resp.output_text
    output = getattr(resp, "output", None)
    if not output:
        return ""
    chunks: List[str] = []
    for item in output:
        content = getattr(item, "content", None) or item.get("content", []) if isinstance(item, dict) else []
        for part in content:
            part_type = getattr(part, "type", None) or part.get("type")
            if part_type == "output_text":
                text = getattr(part, "text", None) or part.get("text", "")
                if text:
                    chunks.append(text)
    return "\n".join(chunks).strip()


def responses_json(
    *,
    schema_name: str,
    schema: Dict[str, Any],
    user_prompt: str,
    system_prompt: Optional[str] = None,
    model: str = OPENAI_TEXT_MODEL,
) -> Dict[str, Any]:
    client = get_openai_client()
    text_format = {
        "type": "json_schema",
        "name": schema_name,
        "schema": schema,
        "strict": True,
    }
    input_payload = _build_input(system_prompt, user_prompt)

    parse_method = getattr(client.responses, "parse", None)
    if callable(parse_method):
        resp = parse_method(
            model=model,
            input=input_payload,
            text={"format": text_format},
            store=False,
        )
        parsed = getattr(resp, "output_parsed", None)
        if parsed is not None:
            return parsed

    resp = client.responses.create(
        model=model,
        input=input_payload,
        text={"format": text_format},
        store=False,
    )
    output_text = _response_text(resp)
    return json.loads(output_text) if output_text else {}


def responses_text(
    *,
    user_prompt: str,
    system_prompt: Optional[str] = None,
    model: str = OPENAI_TEXT_MODEL,
) -> str:
    client = get_openai_client()
    resp = client.responses.create(
        model=model,
        input=_build_input(system_prompt, user_prompt),
        store=False,
    )
    return _response_text(resp)
