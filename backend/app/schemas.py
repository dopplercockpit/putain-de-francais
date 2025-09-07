## backend/app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IngestText(BaseModel):
    user_id: str
    text: str
    context: Optional[Dict[str, Any]] = None

class IngestAudio(BaseModel):
    user_id: str
    audio_url: str
    context: Optional[Dict[str, Any]] = None

class DrillAnswer(BaseModel):
    user_id: str
    drill_id: str
    quality: int = Field(ge=0, le=5)
    response: Optional[Dict[str, Any]] = None

class DailyBiteItem(BaseModel):
    kind: str
    payload: Dict[str, Any]

class DailyBite(BaseModel):
    warmup: DailyBiteItem
    drill: DailyBiteItem
    roleplay: DailyBiteItem


