'use client'
import { useState } from 'react'
import { analyzeContext } from '../lib/api'

const scenarios = [
  {
    key: 'cafe_casual',
    label: 'Cafe with friends',
    context: { situation: 'cafe', formality: 2, relationship: 'friends' },
    prompt: 'Ask a friend to grab a coffee after class.',
  },
  {
    key: 'work_email',
    label: 'Work email',
    context: { situation: 'email', formality: 4, relationship: 'coworker' },
    prompt: 'Ask to reschedule a meeting.',
  },
  {
    key: 'texting_friend',
    label: 'Texting a friend',
    context: { situation: 'text', formality: 1, relationship: 'close_friend' },
    prompt: 'Say you are running late and apologize.',
  },
]

export default function ContextualPractice(){
  const user_level = 'B1'
  const [scenarioKey, setScenarioKey] = useState(scenarios[0].key)
  const [text, setText] = useState('')
  const [result, setResult] = useState<any>(null)
  const scenario = scenarios.find(s => s.key === scenarioKey) || scenarios[0]

  async function analyze(){
    const res = await analyzeContext(text, scenario.context, user_level)
    setResult(res)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <select
          className="px-3 py-2 text-black"
          value={scenarioKey}
          onChange={e => setScenarioKey(e.target.value)}
        >
          {scenarios.map(s => <option key={s.key} value={s.key}>{s.label}</option>)}
        </select>
        <span className="text-sm opacity-70">Level {user_level}</span>
      </div>
      <div className="p-3 rounded border border-white/10 bg-white/5">
        <div className="text-xs uppercase opacity-60">Prompt</div>
        <div>{scenario.prompt}</div>
      </div>
      <textarea
        className="w-full px-3 py-2 text-black"
        rows={3}
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Type your response in French..."
      />
      <button onClick={analyze} className="px-3 py-2 rounded bg-white text-black">Analyze</button>
      {result && (
        <div className="p-4 rounded border border-white/10 bg-white/5 space-y-2">
          <div className="text-sm">Score: <b>{result.score}</b> / 10</div>
          <div className="text-sm">Appropriate: <b>{String(result.appropriate)}</b></div>
          <div className="text-sm">Register: <b>{result.register_note}</b></div>
          {result.natural_alternative && (
            <div className="text-sm">
              Native alternative: <span className="italic">{result.natural_alternative}</span>
            </div>
          )}
          {result.explanation && <div className="text-sm opacity-80">{result.explanation}</div>}
          {result.issues?.length ? (
            <ul className="text-sm list-disc pl-5">
              {result.issues.map((issue: string, i: number) => <li key={i}>{issue}</li>)}
            </ul>
          ) : null}
        </div>
      )}
    </div>
  )
}
