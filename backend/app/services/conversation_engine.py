import uuid
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import ConversationSession, ConversationTurn
from .openai_client import responses_json


SCENARIOS: Dict[str, Dict[str, Any]] = {
    "cafe": {
        "title": "Cafe order",
        "context": {
            "situation": "ordering at a cafe",
            "relationship": "customer to barista",
            "setting": "casual",
        },
        "opening_line": "Bonjour ! Qu'est-ce que je vous sers ?",
    },
    "bakery": {
        "title": "Bakery order",
        "context": {
            "situation": "ordering at a bakery",
            "relationship": "customer to baker",
            "setting": "casual",
        },
        "opening_line": "Bonjour ! Vous désirez ?",
    },
}

UTTERANCE_ANALYSIS_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "ai_message": {"type": "string"},
        "correction": {"type": "string"},
        "understood": {"type": "boolean"},
        "issues": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["ai_message", "correction", "understood", "issues"],
    "additionalProperties": False,
}

SUMMARY_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "strengths": {"type": "array", "items": {"type": "string"}},
        "error_patterns": {"type": "array", "items": {"type": "string"}},
        "focus_areas": {"type": "array", "items": {"type": "string"}},
        "overall_score": {"type": "number"},
    },
    "required": ["strengths", "error_patterns", "focus_areas", "overall_score"],
    "additionalProperties": False,
}


def _scenario_for_key(key: str) -> Dict[str, Any]:
    return SCENARIOS.get(key, SCENARIOS["cafe"])


def _next_turn_index(db: Session, session_id: str) -> int:
    latest = (
        db.execute(
            select(ConversationTurn.turn_index)
            .where(ConversationTurn.session_id == session_id)
            .order_by(ConversationTurn.turn_index.desc())
            .limit(1)
        )
        .scalars()
        .first()
    )
    return (latest or 0) + 1


def _store_turn(
    db: Session,
    session_id: str,
    turn_index: int,
    speaker: str,
    text: str,
    correction: str | None = None,
    meta: Dict[str, Any] | None = None,
) -> ConversationTurn:
    turn = ConversationTurn(
        id=str(uuid.uuid4()),
        session_id=session_id,
        turn_index=turn_index,
        speaker=speaker,
        text=text,
        correction=correction,
        meta=meta or {},
        created_at=datetime.utcnow(),
    )
    db.add(turn)
    return turn


async def start_conversation(
    db: Session,
    user_id: str,
    scenario_key: str,
    user_level: str = "B1",
    corrections_mode: str = "inline",
) -> Dict[str, Any]:
    scenario = _scenario_for_key(scenario_key)
    session = ConversationSession(
        id=str(uuid.uuid4()),
        user_id=user_id,
        scenario_key=scenario_key,
        user_level=user_level,
        corrections_mode=corrections_mode,
        created_at=datetime.utcnow(),
    )
    db.add(session)
    opening = scenario.get("opening_line", "Bonjour !")
    _store_turn(db, session.id, 1, "ai", opening, None, {"scenario": scenario})
    db.commit()
    return {
        "session_id": session.id,
        "scenario": scenario,
        "ai_message": opening,
        "turn_count": 1,
    }


async def process_user_response(
    db: Session,
    session_id: str,
    user_text: str,
    user_level: str = "B1",
    max_turns: int = 10,
) -> Dict[str, Any]:
    session = db.get(ConversationSession, session_id)
    if not session:
        return {"ai_message": "", "correction": "", "understood": False, "turn_count": 0, "continue": False}

    scenario = _scenario_for_key(session.scenario_key)
    turn_index = _next_turn_index(db, session_id)
    _store_turn(db, session_id, turn_index, "user", user_text)

    system = (
        "You are a native French barista roleplaying a conversation. "
        "Respond naturally in French, keeping it concise. Also provide a correction "
        "of the user's French (if needed) and whether you understood them. "
        "Return JSON only with ai_message, correction, understood, issues."
    )
    user_prompt = (
        f"Scenario context: {scenario['context']}\n"
        f"User level: {user_level}\n"
        f"User said: {user_text}\n"
        "Return the structured reply."
    )
    analysis = responses_json(
        schema_name="conversation_turn",
        schema=UTTERANCE_ANALYSIS_SCHEMA,
        system_prompt=system,
        user_prompt=user_prompt,
    )

    ai_reply = analysis.get("ai_message") or "D'accord."

    ai_turn_index = turn_index + 1
    _store_turn(
        db,
        session_id,
        ai_turn_index,
        "ai",
        ai_reply,
        analysis.get("correction"),
        {"issues": analysis.get("issues", []), "understood": analysis.get("understood")},
    )
    db.commit()
    continue_chat = ai_turn_index < max_turns
    return {
        "ai_message": ai_reply,
        "correction": analysis.get("correction"),
        "understood": analysis.get("understood"),
        "turn_count": ai_turn_index,
        "continue": continue_chat,
    }


async def end_conversation(db: Session, session_id: str) -> Dict[str, Any]:
    session = db.get(ConversationSession, session_id)
    if not session:
        return {"strengths": [], "error_patterns": [], "focus_areas": [], "overall_score": 0}

    turns = (
        db.execute(
            select(ConversationTurn)
            .where(ConversationTurn.session_id == session_id)
            .order_by(ConversationTurn.turn_index.asc())
        )
        .scalars()
        .all()
    )
    transcript = "\n".join([f"{t.speaker}: {t.text}" for t in turns])
    system = (
        "You are a French tutor. Summarize the learner performance. "
        "Return JSON with strengths, error_patterns, focus_areas, overall_score."
    )
    user_prompt = f"Transcript:\n{transcript}\nReturn the summary JSON."
    summary = responses_json(
        schema_name="conversation_summary",
        schema=SUMMARY_SCHEMA,
        system_prompt=system,
        user_prompt=user_prompt,
    )

    session.ended_at = datetime.utcnow()
    db.commit()
    return summary
