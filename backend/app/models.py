from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from datetime import datetime
from ..db import Base

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
