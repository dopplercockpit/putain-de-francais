## backend/app/services/llm.py

from typing import Any, Dict, List

from .openai_client import responses_json


ANALYSIS_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "meaning": {"type": "string"},
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue": {"type": "string"},
                    "example": {"type": "string"},
                    "fix": {"type": "string"},
                    "tag": {"type": "string"},
                },
                "required": ["issue", "example", "fix", "tag"],
                "additionalProperties": False,
            },
        },
        "cefr_estimate": {"type": "string"},
        "register": {"type": "string"},
    },
    "required": ["meaning", "errors", "cefr_estimate", "register"],
    "additionalProperties": False,
}

DRILLS_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "drills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "kind": {"type": "string"},
                    "prompt": {"type": "string"},
                    "answer_key": {"type": "object", "additionalProperties": True},
                },
                "required": ["kind", "prompt", "answer_key"],
                "additionalProperties": False,
            },
            "minItems": 1,
        }
    },
    "required": ["drills"],
    "additionalProperties": False,
}


async def analyze_utterance(text: str) -> Dict[str, Any]:
    system = (
        "You are a French tutor. Analyze the learner utterance and return JSON only. "
        "Summarize meaning, list errors with fixes, estimate CEFR, and note register."
    )
    user = f"Utterance:\n{text}\nReturn the analysis JSON."
    return responses_json(
        schema_name="utterance_analysis",
        schema=ANALYSIS_SCHEMA,
        system_prompt=system,
        user_prompt=user,
    )


async def generate_utterance_drills(
    utterance_text: str,
    analysis: Dict[str, Any],
    max_drills: int = 3,
) -> List[Dict[str, Any]]:
    system = (
        "You are a French tutor. Create short, corrective drills. "
        "Return JSON only with 'drills' array. Each drill has kind, prompt, answer_key."
    )
    user = (
        "Utterance:\n"
        f"{utterance_text}\n\n"
        f"Analysis:\n{analysis}\n\n"
        f"Create up to {max_drills} drills."
    )
    payload = responses_json(
        schema_name="utterance_drills",
        schema=DRILLS_SCHEMA,
        system_prompt=system,
        user_prompt=user,
    )
    drills = payload.get("drills", [])
    return drills[:max_drills]


async def generate_daily_bite(context: dict) -> dict:
    # TODO: replace with real implementation
    return {
        "warmup": {"kind": "shadow", "payload": {"text": "Bonjour, je souhaiterais prendre rendez-vous."}},
        "drill": {"kind": "cloze", "payload": {"prompt": "Je vais ___ medecin.", "answer": "chez le"}},
        "roleplay": {"kind": "roleplay", "payload": {"situation": "Appeler l'administration scolaire", "turns": 3}},
    }
