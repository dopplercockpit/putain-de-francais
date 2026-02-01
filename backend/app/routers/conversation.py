from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.conversation_engine import (
    end_conversation,
    process_user_response,
    start_conversation,
)
from app.db import get_db

router = APIRouter(prefix="/conversation", tags=["conversation"])


class ConversationStartRequest(BaseModel):
    user_id: str
    scenario_key: str
    user_level: str = "B1"
    corrections_mode: str = "inline"


class ConversationRespondRequest(BaseModel):
    session_id: str
    user_text: str
    user_level: str = "B1"


class ConversationEndRequest(BaseModel):
    session_id: str


@router.post("/start")
async def start(payload: ConversationStartRequest, db: Session = Depends(get_db)):
    return await start_conversation(
        db,
        user_id=payload.user_id,
        scenario_key=payload.scenario_key,
        user_level=payload.user_level,
        corrections_mode=payload.corrections_mode,
    )


@router.post("/respond")
async def respond(payload: ConversationRespondRequest, db: Session = Depends(get_db)):
    return await process_user_response(
        db,
        session_id=payload.session_id,
        user_text=payload.user_text,
        user_level=payload.user_level,
    )


@router.post("/end")
async def end(payload: ConversationEndRequest, db: Session = Depends(get_db)):
    return await end_conversation(db, session_id=payload.session_id)
