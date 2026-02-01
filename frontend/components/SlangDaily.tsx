'use client'
import { useEffect, useState } from 'react'
import { checkSlangUsage, getDailySlang } from '../lib/api'

export default function SlangDaily(){
  const user_id = 'josh'
  const [daily, setDaily] = useState<any>(null)
  const [attempt, setAttempt] = useState('')
  const [feedback, setFeedback] = useState<any>(null)

  useEffect(() => {
    getDailySlang(user_id).then(setDaily)
  }, [])

  async function check(){
    if (!daily) return
    const res = await checkSlangUsage(user_id, attempt, { situation: 'texting_friend' })
    setFeedback(res)
  }

  return (
    <div className="space-y-4">
      {daily ? (
        <div className="p-4 rounded border border-white/10 bg-white/5 space-y-2">
          <div className="text-xs uppercase opacity-60">Daily slang</div>
          <div className="text-lg font-bold">{daily.expression}</div>
          <div className="text-sm opacity-80">Literal: {daily.literal}</div>
          <div className="text-sm opacity-80">Meaning: {daily.meaning}</div>
          <div className="text-sm opacity-80">Example: {daily.example}</div>
          <div className="text-sm opacity-80">Usage: {daily.usage_note}</div>
        </div>
      ) : (
        <div className="opacity-70">Loading slang...</div>
      )}

      <div className="space-y-2">
        <div className="text-sm">Try using the expression in a sentence:</div>
        <input
          className="w-full px-3 py-2 text-black"
          value={attempt}
          onChange={e => setAttempt(e.target.value)}
          placeholder="Write a short sentence..."
        />
        <button onClick={check} className="px-3 py-2 rounded bg-white text-black">Check usage</button>
      </div>

      {feedback && (
        <div className="p-3 rounded border border-white/10 bg-white/5 text-sm space-y-2">
          <div>Detected: {feedback.slang_detected?.join(', ') || 'none'}</div>
          <div>Appropriate: {String(feedback.appropriate_usage)}</div>
          <div>{feedback.feedback}</div>
        </div>
      )}
    </div>
  )
}
