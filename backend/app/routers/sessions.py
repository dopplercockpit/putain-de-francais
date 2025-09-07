## backend/app/routers/sessions.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db
from ..models import Session as Sess
from datetime import datetime
import uuid

router = APIRouter(prefix="/session", tags=["session"])

@router.post("/start")
def start_session(user_id: str, db: Session = Depends(get_db)):
    s = Sess(id=str(uuid.uuid4()), user_id=user_id, started_at=datetime.utcnow())
    db.add(s); db.commit()
    return {"session_id": s.id}

@router.post("/end")
def end_session(session_id: str, db: Session = Depends(get_db)):
    s = db.get(Sess, session_id)
    s.ended_at = datetime.utcnow()
    db.add(s); db.commit()
    return {"ok": True}

