## README.md (quick start)

```
# Quick Start
cp .env.example .env
# Edit keys

# Start services
docker compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000

# Next steps
- Implement Whisper in stt.py
- Wire real LLM prompts in llm.py
- Replace hardcoded DailyBite with /daily-bite route (generator in llm.py)
- Add auth (Supabase) and per-user storage
```
