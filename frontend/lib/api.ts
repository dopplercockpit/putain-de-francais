// frontend/lib/api.ts

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getDailyBite(user_id: string) {
  const r = await fetch(`${API}/daily-bite?user_id=${user_id}`);
  return r.json();
}

export async function submitDrill(payload: any) {
  const r = await fetch(`${API}/submit/drill`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return r.json();
}

export async function ingestText(user_id: string, text: string, context?: any) {
  const r = await fetch(`${API}/ingest/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, text, context }),
  });
  return r.json();
}

