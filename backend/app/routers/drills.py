from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import DrillAnswer
from ..db import get_db
from ..models import Drill
from ..services.scheduler import schedule_from
from datetime import datetime

router = APIRouter(prefix="/submit", tags=["drills"])

@router.post("/drill")
def submit_drill(payload: DrillAnswer, db: Session = Depends(get_db)):
    dr = db.get(Drill, payload.drill_id)
    if not dr or dr.user_id != payload.user_id:
        raise HTTPException(status_code=404, detail="Drill not found")
    ease, interval, due_at = schedule_from(datetime.utcnow(), dr.ease, dr.interval, payload.quality)
    dr.ease, dr.interval, dr.reps, dr.last_result, dr.due_at = ease, interval, dr.reps + 1, payload.quality, due_at
    db.add(dr); db.commit()
    return {"next_due": dr.due_at, "interval_days": dr.interval, "ease": dr.ease}
