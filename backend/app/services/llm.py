## backend/app/services/llm.py (stubs)

import httpx

from ..core.config import OPENAI_API_KEY, OPENAI_TEXT_MODEL

async def diagnose_and_create_drills(text: str, context: dict | None = None) -> dict:
    # Placeholder — call your LLM with a tightly-scoped system prompt
    # Return: {diagnosis: [...], micro_drills: [...], success_criteria: [...]}
    return {
        "diagnosis": [
            {"issue":"préposition","example":"Je vais à la médecin","fix":"chez le médecin","tag":"preposition"}
        ],
        "micro_drills": [
            {"id":"d1","kind":"cloze","prompt":"Je vais ___ médecin.","answer_key":{"text":"chez le"},"tags":["preposition"]}
        ],
        "success_criteria": ["0 erreurs de préposition dans 5 phrases"]
    }

async def generate_daily_bite(context: dict) -> dict:
    # Return three items minimal
    return {
        "warmup": {"kind":"shadow","payload":{"text":"Bonjour, je souhaiterais prendre rendez-vous."}},
        "drill": {"kind":"cloze","payload":{"prompt":"Je vais ___ médecin.","answer":"chez le"}},
        "roleplay": {"kind":"roleplay","payload":{"situation":"Appeler l'administration scolaire","turns":3}}
    }


