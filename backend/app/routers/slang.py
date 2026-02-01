from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.schemas import SlangUsageCheckRequest
from app.services.slang_teacher import SlangTeacher
from app.db import get_db

router = APIRouter(prefix="/slang", tags=["slang"])


class SlangPracticeRequest(BaseModel):
    expression_id: str
    drill_type: str = "usage_choice"


@router.get("/daily")
async def get_daily_slang(
    user_id: str,
    user_level: str = "B1",
    target_region: str = "France",
    db: Session = Depends(get_db),
):
    teacher = SlangTeacher()
    return await teacher.get_daily_slang(db, user_id, user_level, target_region)


@router.post("/practice")
async def practice_slang(payload: SlangPracticeRequest, db: Session = Depends(get_db)):
    teacher = SlangTeacher()
    return await teacher.generate_slang_drill(db, payload.expression_id, payload.drill_type)


@router.post("/check-usage")
async def check_slang_usage(payload: SlangUsageCheckRequest, db: Session = Depends(get_db)):
    teacher = SlangTeacher()
    return await teacher.detect_slang_in_utterance(
        db,
        text=payload.text,
        context=payload.context,
        user_id=payload.user_id,
    )
