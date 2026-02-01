from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Ensure pgvector extension exists (safe if already installed)
try:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
except Exception as e:
    # Log-friendly, but don't hard crash in dev
    print("[warn] could not ensure pgvector extension:", e)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
