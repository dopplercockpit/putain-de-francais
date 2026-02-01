from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    cefr_target = Column(String, default="C1")
    tone_preference = Column(String, default="spicy")
    consent_sources = Column(ARRAY(String), default=[])

class Source(Base):
    __tablename__ = "sources"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    kind = Column(String)
    uri = Column(String)
    last_ingested_at = Column(DateTime)

class Utterance(Base):
    __tablename__ = "utterances"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    text = Column(Text)
    audio_url = Column(String)
    lang = Column(String, default="fr")
    ts = Column(DateTime, default=datetime.utcnow)
    context_meta = Column(JSON, default={})
    # 3072 dims for text-embedding-3-large
    embedding = Column(Vector(3072))

class Error(Base):
    __tablename__ = "errors"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    utterance_id = Column(String, ForeignKey("utterances.id"))
    tags = Column(ARRAY(String), default=[])
    cefr_area = Column(String)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Drill(Base):
    __tablename__ = "drills"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    kind = Column(String)  # cloze|transform|minimal_pair|roleplay
    prompt = Column(Text)
    answer_key = Column(JSON)
    tags = Column(ARRAY(String), default=[])
    from_error_id = Column(String, ForeignKey("errors.id"), nullable=True)
    due_at = Column(DateTime, default=datetime.utcnow)
    ease = Column(Float, default=2.5)
    interval = Column(Integer, default=0)  # days
    reps = Column(Integer, default=0)
    last_result = Column(Integer, default=0)  # 0..5

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    metrics = Column(JSON, default={})

class Rubric(Base):
    __tablename__ = "rubrics"
    id = Column(String, primary_key=True)
    name = Column(String)
    jsonb = Column(JSON)

class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    type = Column(String)
    payload = Column(JSON)
    ts = Column(DateTime, default=datetime.utcnow)

class Context(Base):
    __tablename__ = "contexts"
    id = Column(String, primary_key=True)
    name = Column(String)
    formality_level = Column(Integer)
    typical_phrases = Column(ARRAY(String))
    avoid_phrases = Column(ARRAY(String))
    cultural_notes = Column(JSON)

class ContextualUtterance(Base):
    __tablename__ = "contextual_utterances"
    id = Column(String, primary_key=True)
    utterance_id = Column(String, ForeignKey("utterances.id"))
    context_id = Column(String, ForeignKey("contexts.id"))
    appropriateness_score = Column(Float)
    suggested_alternative = Column(Text)
    issues = Column(JSON)

class SlangExpression(Base):
    __tablename__ = "slang_expressions"
    id = Column(String, primary_key=True)
    expression = Column(String)
    literal_meaning = Column(String)
    english_equivalent = Column(String)
    formality_level = Column(Integer)
    age_demographic = Column(String)
    region = Column(String)
    usage_frequency = Column(String)
    example_sentences = Column(ARRAY(String))
    avoid_contexts = Column(ARRAY(String))

class UserSlangProgress(Base):
    __tablename__ = "user_slang_progress"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    expression_id = Column(String, ForeignKey("slang_expressions.id"))
    exposure_count = Column(Integer, default=0)
    successful_usage = Column(Integer, default=0)
    last_practiced = Column(DateTime)
    confidence_score = Column(Float)

class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    scenario_key = Column(String)
    user_level = Column(String)
    corrections_mode = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

class ConversationTurn(Base):
    __tablename__ = "conversation_turns"
    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey("conversation_sessions.id"))
    turn_index = Column(Integer)
    speaker = Column(String)
    text = Column(Text)
    correction = Column(Text, nullable=True)
    meta = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
