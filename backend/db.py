from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DATABASE_URL = os.getenv("POSTGRES_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/pdf")
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

from sqlalchemy import text
# Ensure pgvector extension exists (safe if already installed)
try:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
except Exception as e:
    # Log-friendly, but don't hard crash in dev
    print("[warn] could not ensure pgvector extension:", e)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
