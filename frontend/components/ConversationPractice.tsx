'use client'
import { useState } from 'react'
import { endConversation, respondConversation, startConversation } from '../lib/api'

const scenarios = [
  { key: 'cafe', label: 'Cafe order' },
  { key: 'bakery', label: 'Bakery order' },
]

type Msg = { speaker: 'user' | 'ai'; text: string; correction?: string }

export default function ConversationPractice(){
  const user_id = 'josh'
  const [scenarioKey, setScenarioKey] = useState('cafe')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Msg[]>([])
  const [userText, setUserText] = useState('')
  const [summary, setSummary] = useState<any>(null)

  async function start(){
    const res = await startConversation(user_id, scenarioKey)
    setSessionId(res.session_id)
    setMessages([{ speaker: 'ai', text: res.ai_message }])
    setSummary(null)
  }

  async function send(){
    if (!sessionId) return
    const nextMessages = [...messages, { speaker: 'user', text: userText }]
    setMessages(nextMessages)
    setUserText('')
    const res = await respondConversation(sessionId, userText)
    setMessages([...nextMessages, { speaker: 'ai', text: res.ai_message, correction: res.correction }])
  }

  async function end(){
    if (!sessionId) return
    const res = await endConversation(sessionId)
    setSummary(res)
    setSessionId(null)
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-3 items-center">
        <select className="px-3 py-2 text-black" value={scenarioKey} onChange={e => setScenarioKey(e.target.value)}>
          {scenarios.map(s => <option key={s.key} value={s.key}>{s.label}</option>)}
        </select>
        <button onClick={start} className="px-3 py-2 rounded bg-white text-black">Start</button>
        <button onClick={end} className="px-3 py-2 rounded bg-white text-black">End</button>
      </div>

      <div className="space-y-2">
        {messages.map((m, i) => (
          <div key={i} className={`p-3 rounded ${m.speaker === 'ai' ? 'bg-white/10' : 'bg-white/5'}`}>
            <div className="text-xs uppercase opacity-60">{m.speaker}</div>
            <div>{m.text}</div>
            {m.correction && <div className="text-xs opacity-70">Correction: {m.correction}</div>}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 px-3 py-2 text-black"
          value={userText}
          onChange={e => setUserText(e.target.value)}
          placeholder="Type your reply..."
        />
        <button onClick={send} className="px-3 py-2 rounded bg-white text-black">Send</button>
      </div>

      {summary && (
        <div className="p-4 rounded border border-white/10 bg-white/5 space-y-2 text-sm">
          <div><b>Strengths:</b> {summary.strengths?.join(', ')}</div>
          <div><b>Errors:</b> {summary.error_patterns?.join(', ')}</div>
          <div><b>Focus:</b> {summary.focus_areas?.join(', ')}</div>
          <div><b>Score:</b> {summary.overall_score}</div>
        </div>
      )}
    </div>
  )
}
