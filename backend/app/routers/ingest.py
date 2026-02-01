from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from ..schemas import IngestText, IngestAudio
from ..models import Utterance, Drill
from ..services.llm import analyze_utterance, generate_utterance_drills
from ..services.stt import transcribe, transcribe_upload
from ...db import get_db
from datetime import datetime
import json
import uuid

router = APIRouter(prefix="/ingest", tags=["ingest"])


def _build_context_meta(context: dict | None, analysis: dict) -> dict:
    meta = {"analysis": analysis}
    if context:
        meta["context"] = context
    return meta


def _persist_drills(db: Session, user_id: str, drills_payload: list[dict]) -> list[Drill]:
    drills: list[Drill] = []
    for d in drills_payload:
        dr = Drill(
            id=str(uuid.uuid4()),
            user_id=user_id,
            kind=d.get("kind", "cloze"),
            prompt=d.get("prompt", ""),
            answer_key=d.get("answer_key", {}),
            tags=d.get("tags", []),
        )
        db.add(dr)
        drills.append(dr)
    return drills


@router.post("/text")
async def ingest_text(payload: IngestText, db: Session = Depends(get_db)):
    utt_id = str(uuid.uuid4())
    analysis = await analyze_utterance(payload.text)
    utt = Utterance(
        id=utt_id,
        user_id=payload.user_id,
        text=payload.text,
        lang="fr",
        ts=datetime.utcnow(),
        context_meta=_build_context_meta(payload.context, analysis),
    )
    db.add(utt)
    drills_payload = await generate_utterance_drills(payload.text, analysis)
    drills = _persist_drills(db, payload.user_id, drills_payload)
    db.commit()
    return {
        "utterance": {"id": utt_id, "text": payload.text, "analysis": analysis},
        "drills": [
            {"id": d.id, "kind": d.kind, "prompt": d.prompt, "answer_key": d.answer_key}
            for d in drills
        ],
    }


# Deprecated: use /ingest/audio-file for UploadFile-based transcription
@router.post("/audio")
async def ingest_audio(payload: IngestAudio, db: Session = Depends(get_db)):
    text = await transcribe(payload.audio_url)
    nested = IngestText(user_id=payload.user_id, text=text, context=payload.context)
    return await ingest_text(nested, db)


@router.post("/audio-file")
async def ingest_audio_file(
    user_id: str = Form(...),
    audio: UploadFile = File(...),
    context: str | None = Form(None),
    db: Session = Depends(get_db),
):
    context_payload = None
    if context:
        try:
            context_payload = json.loads(context)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail="context must be valid JSON") from exc

    text = await transcribe_upload(audio)
    analysis = await analyze_utterance(text)
    utt_id = str(uuid.uuid4())
    utt = Utterance(
        id=utt_id,
        user_id=user_id,
        text=text,
        lang="fr",
        ts=datetime.utcnow(),
        context_meta=_build_context_meta(context_payload, analysis),
    )
    db.add(utt)

    drills_payload = await generate_utterance_drills(text, analysis)
    drills = _persist_drills(db, user_id, drills_payload)
    db.commit()

    return {
        "utterance": {"id": utt_id, "text": text, "analysis": analysis},
        "drills": [
            {"id": d.id, "kind": d.kind, "prompt": d.prompt, "answer_key": d.answer_key}
            for d in drills
        ],
    }
