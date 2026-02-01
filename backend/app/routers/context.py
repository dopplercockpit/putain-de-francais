from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import ContextAnalysisRequest
from ..services.context_analyzer import analyze_contextual_fit
from ...db import get_db

router = APIRouter(prefix="/context", tags=["context"])


@router.post("/analyze")
async def analyze_context(payload: ContextAnalysisRequest, db: Session = Depends(get_db)):
    return await analyze_contextual_fit(
        text=payload.text,
        context=payload.context,
        user_cefr_level=payload.user_level,
        db=db,
    )
