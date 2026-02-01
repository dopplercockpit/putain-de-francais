from typing import Any, Dict, Optional
import uuid

from sqlalchemy.orm import Session

from ..models import ContextualUtterance
from .openai_client import responses_json


CONTEXT_ANALYSIS_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "appropriate": {"type": "boolean"},
        "score": {"type": "number"},
        "issues": {"type": "array", "items": {"type": "string"}},
        "natural_alternative": {"type": "string"},
        "explanation": {"type": "string"},
        "register_note": {"type": "string"},
    },
    "required": [
        "appropriate",
        "score",
        "issues",
        "natural_alternative",
        "explanation",
        "register_note",
    ],
    "additionalProperties": False,
}


async def analyze_contextual_fit(
    text: str,
    context: Dict[str, Any],
    user_cefr_level: str = "B1",
    db: Optional[Session] = None,
    utterance_id: Optional[str] = None,
    context_id: Optional[str] = None,
) -> Dict[str, Any]:
    system = (
        "You are a native French coach with strong register sensitivity. "
        "Assess whether the utterance fits the context and provide a natural alternative."
    )
    user = (
        "Analyze this French in context and return JSON.\n"
        f"Utterance: {text}\n"
        f"Context: {context}\n"
        f"User level: {user_cefr_level}\n"
        "Return the structured analysis."
    )
    result = responses_json(
        schema_name="contextual_fit",
        schema=CONTEXT_ANALYSIS_SCHEMA,
        system_prompt=system,
        user_prompt=user,
    )

    if db and utterance_id and context_id:
        contextual = ContextualUtterance(
            id=str(uuid.uuid4()),
            utterance_id=utterance_id,
            context_id=context_id,
            appropriateness_score=result.get("score"),
            suggested_alternative=result.get("natural_alternative"),
            issues={
                "issues": result.get("issues", []),
                "explanation": result.get("explanation", ""),
                "register_note": result.get("register_note", ""),
            },
        )
        db.add(contextual)
        db.commit()

    return result
