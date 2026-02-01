'use client'
import { useState } from 'react'
import Recorder from './Recorder'
import { ingestAudioFile } from '../lib/api'

export default function PronunciationPractice(){
  const user_id = 'josh'
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  async function handleBlob(blob: Blob){
    setLoading(true)
    try {
      const res = await ingestAudioFile(user_id, blob, { mode: 'pronunciation' })
      setResult(res)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <Recorder onBlob={handleBlob} />
      {loading && <div className="text-sm opacity-70">Transcribing...</div>}
      {result && (
        <div className="p-4 rounded border border-white/10 bg-white/5 space-y-2 text-sm">
          <div><b>Transcript:</b> {result.utterance?.text}</div>
          {result.utterance?.analysis && (
            <div><b>Analysis:</b> {JSON.stringify(result.utterance.analysis)}</div>
          )}
          {result.drills?.length ? (
            <div>
              <b>Drills:</b>
              <ul className="list-disc pl-5">
                {result.drills.map((d: any) => (
                  <li key={d.id}>{d.prompt}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      )}
    </div>
  )
}
