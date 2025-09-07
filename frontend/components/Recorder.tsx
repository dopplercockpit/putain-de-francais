// frontend/components/Recorder.tsx (basic mic capture)

'use client'
import { useEffect, useRef, useState } from 'react'

export default function Recorder({ onBlob }: { onBlob: (b: Blob) => void }){
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
    mr.onstop = () => onBlob(new Blob(chunks, { type: 'audio/webm' }))
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

