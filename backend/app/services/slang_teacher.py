import hashlib
import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import SlangExpression, UserSlangProgress
from .openai_client import responses_json


SLANG_USAGE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "slang_detected": {"type": "array", "items": {"type": "string"}},
        "appropriate_usage": {"type": "boolean"},
        "feedback": {"type": "string"},
        "mastery_boost": {"type": "number"},
    },
    "required": ["slang_detected", "appropriate_usage", "feedback", "mastery_boost"],
    "additionalProperties": False,
}


def seed_slang_if_empty(db: Session) -> int:
    existing = db.execute(select(SlangExpression).limit(1)).scalar_one_or_none()
    if existing:
        return 0

    seed_data = [
        {
            "expression": "C'est ouf",
            "literal_meaning": "C'est fou",
            "english_equivalent": "That's crazy",
            "formality_level": 1,
            "age_demographic": "youth",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["Ce match, c'est ouf !"],
            "avoid_contexts": ["job_interview", "formal_email"],
        },
        {
            "expression": "C'est nickel",
            "literal_meaning": "C'est parfait",
            "english_equivalent": "It's perfect",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["On se retrouve a 18h ? C'est nickel."],
            "avoid_contexts": ["very_formal_speech"],
        },
        {
            "expression": "Ça marche",
            "literal_meaning": "C'est d'accord",
            "english_equivalent": "Sounds good",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["On se voit demain ? Ca marche."],
            "avoid_contexts": ["very_formal_email"],
        },
        {
            "expression": "Grave",
            "literal_meaning": "Tout a fait",
            "english_equivalent": "Totally",
            "formality_level": 1,
            "age_demographic": "youth",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["T'es pret ? Grave."],
            "avoid_contexts": ["formal_meeting"],
        },
        {
            "expression": "Bof",
            "literal_meaning": "Moyen",
            "english_equivalent": "Meh",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["Le film etait bien ? Bof."],
            "avoid_contexts": ["formal_review"],
        },
        {
            "expression": "Ça roule",
            "literal_meaning": "Tout va bien",
            "english_equivalent": "All good",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["Salut, ca roule ?"],
            "avoid_contexts": ["formal_email"],
        },
        {
            "expression": "J'en peux plus",
            "literal_meaning": "Je suis epuise",
            "english_equivalent": "I can't take it anymore",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["Cette semaine, j'en peux plus."],
            "avoid_contexts": ["formal_email"],
        },
        {
            "expression": "Trop bien",
            "literal_meaning": "Vraiment bien",
            "english_equivalent": "So good",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["Ton idee est trop bien."],
            "avoid_contexts": ["formal_report"],
        },
        {
            "expression": "Pas ouf",
            "literal_meaning": "Pas tres bien",
            "english_equivalent": "Not great",
            "formality_level": 1,
            "age_demographic": "youth",
            "region": "France",
            "usage_frequency": "trending",
            "example_sentences": ["Le resto etait pas ouf."],
            "avoid_contexts": ["formal_email"],
        },
        {
            "expression": "Ça me saoule",
            "literal_meaning": "Cela m'ennuie",
            "english_equivalent": "It annoys me",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["Ce retard, ca me saoule."],
            "avoid_contexts": ["formal_email"],
        },
        {
            "expression": "T'inquiete",
            "literal_meaning": "Ne t'inquiete pas",
            "english_equivalent": "Don't worry",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["T'inquiete, ca va aller."],
            "avoid_contexts": ["formal_letter"],
        },
        {
            "expression": "Ça passe",
            "literal_meaning": "C'est acceptable",
            "english_equivalent": "It's okay",
            "formality_level": 2,
            "age_demographic": "general",
            "region": "France",
            "usage_frequency": "common",
            "example_sentences": ["Cette version, ca passe."],
            "avoid_contexts": ["very_formal_report"],
        },
    ]

    for item in seed_data:
        db.add(
            SlangExpression(
                id=str(uuid.uuid4()),
                expression=item["expression"],
                literal_meaning=item["literal_meaning"],
                english_equivalent=item["english_equivalent"],
                formality_level=item["formality_level"],
                age_demographic=item["age_demographic"],
                region=item["region"],
                usage_frequency=item["usage_frequency"],
                example_sentences=item["example_sentences"],
                avoid_contexts=item["avoid_contexts"],
            )
        )
    db.commit()
    return len(seed_data)


class SlangTeacher:
    async def get_daily_slang(
        self,
        db: Session,
        user_id: str,
        user_level: str = "B1",
        target_region: str = "France",
    ) -> Dict[str, Any]:
        query = select(SlangExpression).order_by(SlangExpression.expression)
        expressions = db.execute(query).scalars().all()
        if not expressions:
            return {
                "expression_id": "",
                "expression": "",
                "literal": "",
                "meaning": "",
                "formality": 0,
                "example": "",
                "usage_note": "",
                "region": target_region,
                "similar_expressions": [],
                "practice_scenarios": [],
            }

        filtered = [
            e
            for e in expressions
            if e.region == target_region or e.region == "general" or target_region == "France"
        ]
        if not filtered:
            filtered = expressions

        today = date.today().isoformat()
        seed = f"{user_id}-{today}"
        digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
        index = int(digest, 16) % len(filtered)
        item = filtered[index]
        example = item.example_sentences[0] if item.example_sentences else ""
        usage_note = f"{item.usage_frequency} usage; avoid: {', '.join(item.avoid_contexts or [])}"
        return {
            "expression_id": item.id,
            "expression": item.expression,
            "literal": item.literal_meaning,
            "meaning": item.english_equivalent,
            "formality": item.formality_level,
            "example": example,
            "usage_note": usage_note,
            "region": item.region,
            "similar_expressions": [],
            "practice_scenarios": [],
        }

    async def generate_slang_drill(
        self,
        db: Session,
        expression_id: str,
        drill_type: str = "usage_choice",
    ) -> Dict[str, Any]:
        expr = db.get(SlangExpression, expression_id)
        if not expr:
            return {"kind": "error", "message": "expression not found"}

        if drill_type == "usage_choice":
            return {
                "kind": "multiple_choice",
                "prompt": f"Which response best fits a casual chat? ({expr.expression})",
                "options": [
                    f"{expr.expression} !",
                    f"Je vous remercie pour votre message.",
                    "Ceci est acceptable.",
                    "Je suis satisfait.",
                ],
                "correct_index": 0,
                "explanation": "The slang expression is appropriate in casual contexts.",
            }

        return {
            "kind": "transform",
            "prompt": "Make this sound more casual/natural:",
            "formal_version": f"C'est tres bien.",
            "target_slang": [expr.expression],
            "acceptable_answers": [f"{expr.expression} !"],
            "explanation": "Use the slang expression to sound more natural.",
        }

    async def detect_slang_in_utterance(
        self,
        db: Session,
        text: str,
        context: Dict[str, Any],
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        expressions = db.execute(select(SlangExpression)).scalars().all()
        known = [e.expression for e in expressions][:50]
        system = (
            "You are a native French coach. Detect slang in the utterance and judge "
            "whether it fits the context. Return JSON only."
        )
        user = (
            f"Utterance: {text}\n"
            f"Context: {context}\n"
            f"Known slang list: {known}\n"
            "Return structured detection and feedback."
        )
        result = responses_json(
            schema_name="slang_usage",
            schema=SLANG_USAGE_SCHEMA,
            system_prompt=system,
            user_prompt=user,
        )

        if user_id and result.get("slang_detected"):
            detected_lower = {s.lower() for s in result.get("slang_detected", [])}
            for expr in expressions:
                if expr.expression.lower() in detected_lower:
                    progress = (
                        db.execute(
                            select(UserSlangProgress).where(
                                UserSlangProgress.user_id == user_id,
                                UserSlangProgress.expression_id == expr.id,
                            )
                        )
                        .scalars()
                        .first()
                    )
                    if not progress:
                        progress = UserSlangProgress(
                            id=str(uuid.uuid4()),
                            user_id=user_id,
                            expression_id=expr.id,
                            exposure_count=0,
                            successful_usage=0,
                            confidence_score=0.0,
                        )
                        db.add(progress)
                    progress.exposure_count += 1
                    if result.get("appropriate_usage"):
                        progress.successful_usage += 1
                        progress.confidence_score = min(
                            1.0, (progress.confidence_score or 0.0) + float(result.get("mastery_boost", 0.0))
                        )
                    progress.last_practiced = datetime.utcnow()
            db.commit()

        return result
