import io
from typing import Optional

import httpx
from fastapi import UploadFile

from app.core.config import OPENAI_TRANSCRIBE_MODEL
from .openai_client import get_openai_client

# Transcriptions support whisper-1 and gpt-4o*-transcribe models with a 25 MB file limit.


def _coerce_filename(file_obj, filename: Optional[str]) -> None:
    if not getattr(file_obj, "name", None):
        file_obj.name = filename or "audio"


def _extract_text(resp) -> str:
    text = getattr(resp, "text", None)
    if text is not None:
        return text
    if isinstance(resp, dict):
        return resp.get("text", "")
    return ""


async def transcribe_upload(audio: UploadFile, language: str = "fr") -> str:
    _coerce_filename(audio.file, audio.filename)
    client = get_openai_client()
    resp = client.audio.transcriptions.create(
        model=OPENAI_TRANSCRIBE_MODEL,
        file=audio.file,
        language=language,
    )
    return _extract_text(resp)


async def transcribe(audio_url: str, language: str = "fr") -> str:
    async with httpx.AsyncClient() as http:
        resp = await http.get(audio_url)
        resp.raise_for_status()
        data = io.BytesIO(resp.content)
        _coerce_filename(data, "audio")
    client = get_openai_client()
    transcript = client.audio.transcriptions.create(
        model=OPENAI_TRANSCRIBE_MODEL,
        file=data,
        language=language,
    )
    return _extract_text(transcript)
