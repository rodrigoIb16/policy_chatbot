import { useState } from 'react'

export default function Home() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([])

  const handleSend = async () => {
    if (!query.trim()) return

    const userMessage = { role: 'user', text: query }
    setMessages((prev) => [...prev, userMessage])
    setQuery('')

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: query }),
    })

    const data = await res.json()

    let botText = data.output
    try {
      const parsed = JSON.parse(data.output)
      if (parsed?.output) botText = parsed.output
    } catch (err){
      // leave botText as is
    }

    setMessages((prev) => [...prev, { role: 'bot', text: botText }])
  }

  return (
    <main className="p-6 max-w-xl mx-auto min-h-screen bg-black text-white">
      <h1 className="text-3xl font-bold mb-6 text-center">💬 HRBot</h1>

      <div className="space-y-4 mb-4">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`px-4 py-2 rounded-lg max-w-xs ${
                m.role === 'user' ? 'bg-blue-500 text-white' : 'bg-white text-black'
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 border border-gray-500 bg-gray-900 text-white p-2 rounded"
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={handleSend}>
          Send
        </button>
      </div>
    </main>
  )
}
