from fastapi import FastAPI
from ..db import Base, engine
from .routers import ingest, drills, sessions, progress, daily

app = FastAPI(title="Putain de Français API", version="0.2")

# Create tables (simple dev mode)
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(ingest.router)
app.include_router(drills.router)
app.include_router(sessions.router)
app.include_router(progress.router)
app.include_router(daily.router)

@app.get("/")
def root():
    return {"ok": True}
