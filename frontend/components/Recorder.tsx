// frontend/components/Recorder.tsx (basic mic capture)

'use client'
import { useEffect, useRef, useState } from 'react'

type RecorderProps = {
  onBlob?: (b: Blob) => void
  uploadUrl?: string
  extraFields?: Record<string, string>
  onUploaded?: (data: any) => void
  filename?: string
}

export default function Recorder({
  onBlob,
  uploadUrl,
  extraFields,
  onUploaded,
  filename = 'audio.webm',
}: RecorderProps){
  const mediaRef = useRef<MediaRecorder | null>(null)
  const [rec, setRec] = useState(false)

  useEffect(() => {
    return () => mediaRef.current?.stop()
  }, [])

  async function start(){
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mr = new MediaRecorder(stream)
    const chunks: BlobPart[] = []
    mr.ondataavailable = e => chunks.push(e.data)
    mr.onstop = async () => {
      const blob = new Blob(chunks, { type: 'audio/webm' })
      onBlob?.(blob)
      if (uploadUrl) {
        const body = new FormData()
        body.append('audio', blob, filename)
        if (extraFields) {
          Object.entries(extraFields).forEach(([key, value]) => body.append(key, value))
        }
        const res = await fetch(uploadUrl, { method: 'POST', body })
        const data = await res.json()
        onUploaded?.(data)
      }
    }
    mr.start()
    mediaRef.current = mr
    setRec(true)
  }
  function stop(){ mediaRef.current?.stop(); setRec(false) }

  return (
    <div className="flex gap-3 items-center">
      {!rec ? <button onClick={start} className="px-3 py-2 rounded bg-white text-black">Record</button>
            : <button onClick={stop} className="px-3 py-2 rounded bg-white text-black">Stop</button>}
    </div>
  )
}

