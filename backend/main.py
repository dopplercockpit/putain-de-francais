## backend/app/main.py

from fastapi import FastAPI
from .db import Base, engine
from .routers import ingest, drills, sessions, progress

app = FastAPI(title="Putain de Français API", version="0.1")

Base.metadata.create_all(bind=engine)

app.include_router(ingest.router)
app.include_router(drills.router)
app.include_router(sessions.router)
app.include_router(progress.router)

@app.get("/")
def root():
    return {"ok": True}


