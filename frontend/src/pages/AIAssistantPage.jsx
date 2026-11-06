import { useState } from 'react'

const SUGGESTED_QUESTIONS = [
  'What is the current rockfall risk assessment?',
  'Show me recent sensor anomalies',
  'What does the crown pillar stability data indicate?',
  'Generate a risk summary report',
  'Explain the monitoring coverage for Sector 4',
]

const DEMO_RESPONSES = {
  'What is the current rockfall risk assessment?':
    'Based on the latest telemetry, the overall risk is LOW across all sectors. Sector 1 (West Access Ramp) and Sector 3 (East Rib) show stable conditions. Sectors 2 and 4 show medium risk with 1 recent event each. Sector 5 (Crown Pillar) currently shows critical conditions with 2 recent events requiring attention.',
  'Show me recent sensor anomalies':
    'Recent anomalies detected: Hanging Wall Spall at 13:42 in Sector 2 (ML 0.8, warning), Crown Pillar Shear at 14:18 in Sector 5 (ML 1.2, critical). All other recent events are nominal.',
  'What does the crown pillar stability data indicate?':
    'Crown Pillar (Sector 5) shows critical stability concerns with 2 events in the last 2 hours. The model indicates potential stress redistribution. Sectors 1-4 show nominal to medium stability. Immediate monitoring recommended.',
  'Generate a risk summary report':
    'Demo report generated: Risk levels - Low: 2 sectors, Medium: 2 sectors, Critical: 1 sector. Total events: 3. Recommendations: Increase monitoring frequency in Sector 5, review pillar support design.',
  'Explain the monitoring coverage for Sector 4':
    'Sector 4 (North Wall) has 2 seismometers, 3 accelerometers, and 2 cameras providing 24/7 coverage. Last data refresh: 2 minutes ago. No critical events in the last 24 hours. Medium risk level with 1 recent event',
}

export default function AIAssistantPage() {
  const [messages, setMessages] = useState<Array<{role: 'user' | 'assistant', content: string}>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = (content) => {
    setMessages(prev => prev.concat({role: 'user', content}))
    setInput('')
    setLoading(true)
    // Simulate API call
    setTimeout(() => {
      const lower = content.toLowerCase()
      let response = 'I am unable to process that request at this time, as the AI service is not connected.'
      for (const q of Object.keys(DEMO_RESPONSES)) {
        if (lower.includes(q.toLowerCase())) {
          response = DEMO_RESPONSES[q]
          break
        }
      }
      setMessages(prev => prev.concat({role: 'assistant', content: response}))
      setLoading(false)
    }, 1200)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && input.trim()) {
      sendMessage(input)
    }
  }

  return (
    <div className="flex flex-col w-full px-gutter py-space-sm space-y-space-md max-w-7xl mx-auto">
      <h1 className="scada-page-title">AI Assistant</h1>
      <p className="scada-page-subtitle">GeoAlert AI — Geotechnical monitoring insights</p>
      
      <div className="space-y-2" role="main" aria-live="polite">
        {messages.map((msg, idx) => (
          <div key={idx} className="p-3 rounded-lg border border-outline/30 max-w-lg mx-auto">
            <div className="flex items-start gap-3">
              <span className={msg.role === 'assistant' ? 'w-8 h-8 rounded-full bg-surface-container-high flex items-center justify-center text-on-surface' : 'w-8 h-8 rounded-full bg-primary flex items-center justify-center text-on-primary'}>
                <span className="material-symbols-outlined text-[20px]">
                  {msg.role === 'assistant' ? 'person' : 'insert_emoticon'}
                </span>
              </span>
              <div className={msg.role === 'assistant' ? 'flex-1' : 'bg-primary text-on-primary rounded'}>
                <p className="font-medium">{msg.content}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {loading && (
        <div className="p-3 rounded-lg border border-outline/30 max-w-lg mx-auto">
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-[20px] animate-spin">refresh</span>
            <span>Thinking...</span>
          </div>
        </div>
      )}

      <form
        onSubmit={(e) => {
          e.preventDefault()
          if (input.trim()) sendMessage(input)
        }}
        className="flex gap-2 p-3 rounded-lg border border-outline/30"
        aria-label="Submit AI assistant message"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about rockfall risk, sensor data, or monitoring..."
          disabled={loading}
          className="flex-1 border rounded-lg py-2 px-3 text-on-surface focus:outline-none focus:ring-2 focus:ring-primary"
          aria="input"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading}
          className="scada-btn-primary py-2 px-4 rounded-lg"
          aria="send button"
        >
          <span className="material-symbols-outlined">send</span> Send
        </button>
      </form>
    </div>
  )
}