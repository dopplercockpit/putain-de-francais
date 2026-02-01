'use client'
import { useState } from "react";
import DailyBite from "../components/DailyBite";
import ContextualPractice from "../components/ContextualPractice";
import SlangDaily from "../components/SlangDaily";
import ConversationPractice from "../components/ConversationPractice";
import PronunciationPractice from "../components/PronunciationPractice";

const tabs = [
  { key: "daily", label: "Daily Bite", component: <DailyBite /> },
  { key: "context", label: "Context", component: <ContextualPractice /> },
  { key: "slang", label: "Slang", component: <SlangDaily /> },
  { key: "conversation", label: "Conversation", component: <ConversationPractice /> },
  { key: "pronunciation", label: "Pronunciation", component: <PronunciationPractice /> },
];

export default function Page(){
  const [active, setActive] = useState("daily");
  const current = tabs.find(t => t.key === active) || tabs[0];

  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <div className="text-xs uppercase tracking-[0.3em] opacity-70">Putain de Francais</div>
        <h1 className="text-3xl font-bold">Practice Lab</h1>
        <p className="opacity-70 text-sm">Context, slang, conversation, and pronunciation in one place.</p>
      </header>

      <nav className="flex flex-wrap gap-2">
        {tabs.map(t => (
          <button
            key={t.key}
            onClick={() => setActive(t.key)}
            className={`px-3 py-2 rounded border ${active === t.key ? "bg-white text-black" : "border-white/20 bg-white/5"}`}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <section className="p-4 rounded-xl border border-white/10 bg-gradient-to-br from-white/10 via-white/5 to-transparent">
        {current.component}
      </section>
    </div>
  );
}
