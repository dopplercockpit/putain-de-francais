from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

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

class ContextAnalysisRequest(BaseModel):
    text: str
    context: Dict[str, Any]
    user_level: str

class ContextAnalysisResponse(BaseModel):
    appropriate: bool
    score: float
    issues: List[str]
    natural_alternative: str
    explanation: str
    register_note: str

class SlangDailyResponse(BaseModel):
    expression_id: str
    expression: str
    literal: str
    meaning: str
    formality: int
    example: str
    usage_note: str
    region: Optional[str] = None
    similar_expressions: Optional[List[str]] = None
    practice_scenarios: Optional[List[str]] = None

class SlangUsageCheckRequest(BaseModel):
    user_id: str
    text: str
    context: Dict[str, Any]

class SlangUsageCheckResponse(BaseModel):
    slang_detected: List[str]
    appropriate_usage: bool
    feedback: str
    mastery_boost: float
