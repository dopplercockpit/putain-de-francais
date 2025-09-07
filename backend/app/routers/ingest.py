from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import IngestText, IngestAudio
from ..models import Utterance, Drill
from ..services.llm import diagnose_and_create_drills
from ..services.stt import transcribe
from ...db import get_db
from datetime import datetime
import uuid

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/text")
async def ingest_text(payload: IngestText, db: Session = Depends(get_db)):
    utt_id = str(uuid.uuid4())
    utt = Utterance(
        id=utt_id,
        user_id=payload.user_id,
        text=payload.text,
        lang="fr",
        ts=datetime.utcnow(),
        context_meta=payload.context or {},
    )
    db.add(utt); db.commit()

    diag = await diagnose_and_create_drills(payload.text, payload.context or {})
    drills = []
    for d in diag.get("micro_drills", []):
        dr = Drill(
            id=str(uuid.uuid4()),
            user_id=payload.user_id,
            kind=d.get("kind", "cloze"),
            prompt=d.get("prompt", ""),
            answer_key=d.get("answer_key", {}),
            tags=d.get("tags", []),
        )
        db.add(dr); drills.append(dr)
    db.commit()
    return {"utterance_id": utt_id, "drills": [d.id for d in drills], "diagnosis": diag.get("diagnosis", [])}

@router.post("/audio")
async def ingest_audio(payload: IngestAudio, db: Session = Depends(get_db)):
    text = await transcribe(payload.audio_url)
    nested = IngestText(user_id=payload.user_id, text=text, context=payload.context)
    return await ingest_text(nested, db)
