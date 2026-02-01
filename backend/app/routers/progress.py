from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models import Error, Drill, Utterance
from datetime import datetime, timedelta

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("/weekly")
def weekly(user_id: str, db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=7)
    errs = db.query(Error).filter(Error.user_id==user_id, Error.created_at>=since).count()
    done = db.query(Drill).filter(Drill.user_id==user_id, Drill.reps>0).count()
    due = db.query(Drill).filter(Drill.user_id==user_id, Drill.due_at <= datetime.utcnow()).count()
    return {"errors_logged": errs, "drills_done": done, "drills_due": due}


