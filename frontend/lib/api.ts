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

export async function startConversation(user_id: string, scenario_key: string, user_level = "B1") {
  const r = await fetch(`${API}/conversation/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, scenario_key, user_level }),
  });
  return r.json();
}

export async function respondConversation(session_id: string, user_text: string, user_level = "B1") {
  const r = await fetch(`${API}/conversation/respond`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id, user_text, user_level }),
  });
  return r.json();
}

export async function endConversation(session_id: string) {
  const r = await fetch(`${API}/conversation/end`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id }),
  });
  return r.json();
}

export async function analyzeContext(text: string, context: any, user_level = "B1") {
  const r = await fetch(`${API}/context/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, context, user_level }),
  });
  return r.json();
}

export async function getDailySlang(user_id: string, user_level = "B1", target_region = "France") {
  const params = new URLSearchParams({ user_id, user_level, target_region });
  const r = await fetch(`${API}/slang/daily?${params.toString()}`);
  return r.json();
}

export async function checkSlangUsage(user_id: string, text: string, context: any) {
  const r = await fetch(`${API}/slang/check-usage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, text, context }),
  });
  return r.json();
}

export async function ingestAudioFile(user_id: string, audio: Blob, context?: any) {
  const body = new FormData();
  body.append("user_id", user_id);
  if (context) body.append("context", JSON.stringify(context));
  body.append("audio", audio, "audio.webm");
  const r = await fetch(`${API}/ingest/audio-file`, {
    method: "POST",
    body,
  });
  return r.json();
}

