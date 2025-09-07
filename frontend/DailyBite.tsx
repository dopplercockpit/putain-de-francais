// frontend/components/DailyBite.tsx (MVP)

'use client'
import { useEffect, useState } from 'react'
import { ingestText, submitDrill } from '../lib/api'

export default function DailyBite(){
  const user_id = 'josh'
  const [warmup,setWarmup] = useState<string>('')
  const [prompt,setPrompt] = useState<string>('')
  const [answer,setAnswer] = useState<string>('')
  const [drillId,setDrillId] = useState<string>('')

  useEffect(() => {
    setWarmup('Bonjour, je souhaiterais prendre rendez-vous.')
    setPrompt('Je vais ___ médecin.')
    setAnswer('')
    setDrillId('d1')
  }, [])

  async function check(){
    const quality = (answer.trim().toLowerCase() === 'chez le') ? 5 : 2
    const res = await submitDrill({ user_id, drill_id: drillId, quality, response: { answer } })
    alert(`Next due in ${res.interval_days} days`)
  }

  async function roastThis(){
    await ingestText(user_id, 'Bonjour, je veux un rendez-vous avec la médecin demain svp.', { mode: 'roast' })
    alert('Roasted. Check backend logs for now.')
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


