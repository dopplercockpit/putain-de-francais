from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ..schemas import DailyBite
from ..services.llm import generate_daily_bite

router = APIRouter(prefix="", tags=["daily"])

@router.get("/daily-bite", response_model=DailyBite)
async def daily_bite(user_id: str, db: Session = Depends(get_db)):
    # TODO: use user profile + due drills to build a real bite
    ctx = {"user_id": user_id}
    data = await generate_daily_bite(ctx)
    return data
