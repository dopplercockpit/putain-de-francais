from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..db import Base, engine
from .routers import ingest, drills, sessions, progress, daily

app = FastAPI(title="Putain de Français API", version="0.2")

# 🔥 CORS: allow your dev frontend(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(ingest.router)
app.include_router(drills.router)
app.include_router(sessions.router)
app.include_router(progress.router)
app.include_router(daily.router)

@app.get("/")
def root():
    return {"ok": True}
