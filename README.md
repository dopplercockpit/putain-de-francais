# Putain de Français

## Local Setup

```
# Start services (requires OPENAI_API_KEY in root .env or shell env)
docker compose up --build

# Frontend dev server (optional if running docker frontend)
cd frontend
npm install
npm run dev

# Reset DB (data wipe)
docker compose down -v
```

## Quick Start

```
cp .env.example .env
## Add OPENAI_API_KEY or export it in your shell

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
