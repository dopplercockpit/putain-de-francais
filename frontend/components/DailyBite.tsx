'use client'
import { useEffect, useState } from 'react'
import { ingestText, submitDrill } from '../lib/api'

export default function DailyBite(){
  const user_id = 'josh'
  const [warmup,setWarmup] = useState('Bonjour, je souhaiterais prendre rendez-vous.')
  const [prompt,setPrompt] = useState('Je vais ___ médecin.')
  const [answer,setAnswer] = useState('')
  const [drillId,setDrillId] = useState<string | null>(null)

  async function check(){
    if(!drillId){ alert('Create a drill first (hit Roast This).'); return }
    const quality = (answer.trim().toLowerCase() === 'chez le') ? 5 : 2
    const res = await submitDrill({ user_id, drill_id: drillId, quality, response: { answer } })
    alert(`Saved. Next due in ${res.interval_days} days`)
  }

  async function roastThis(){
    const text = 'Bonjour, je veux un rendez-vous avec la médecin demain svp.'
    const res = await ingestText(user_id, text, { mode: 'roast' })
    if (res?.drills?.length) {
      setDrillId(res.drills[0])
      // optional: adapt the prompt to match the generated drill
      setPrompt('Je vais ___ médecin.')
      alert('Drill created. Now answer it and press Check.')
    } else {
      alert('No drill returned 🤨')
    }
  }

  return (
    <div className="space-y-6">
      <section>
        <h2 className="text-xl font-bold">Warmup (shadow)</h2>
        <p className="text-lg">{warmup}</p>
      </section>
      <section>
        <h2 className="text-xl font-bold">Drill</h2>
        <p className="mb-2">{prompt}</p>
        <input className="px-3 py-2 text-black" value={answer} onChange={e=>setAnswer(e.target.value)} placeholder="your answer"/>
        <button onClick={check} className="ml-3 px-3 py-2 rounded bg-white text-black">Check</button>
      </section>
      <section>
        <button onClick={roastThis} className="px-3 py-2 rounded bg-white text-black">Roast This</button>
      </section>
    </div>
  )
}
