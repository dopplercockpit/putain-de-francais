# Putain de Français

## Local Setup

```
# Start services
docker compose up --build

# Frontend dev server
cd frontend
npm install
npm run dev

# Reset DB (data wipe)
docker compose down -v
```

## Quick Start

```
cp backend/.env.example backend/.env
# Edit keys

# Backend: http://localhost:8000
# Frontend: http://localhost:3000

# Next steps
- Implement Whisper in stt.py
- Wire real LLM prompts in llm.py
- Replace hardcoded DailyBite with /daily-bite route (generator in llm.py)
- Add auth (Supabase) and per-user storage
```
