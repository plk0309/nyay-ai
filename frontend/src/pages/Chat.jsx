import { useState, useRef, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  Scale, Send, Mic, MicOff, Plus, LogOut,
  User, FileText, ChevronRight, Volume2, Loader
} from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [language, setLanguage] = useState('en')
  const [history, setHistory] = useState([])
  const messagesEndRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const currentAudioRef = useRef(null)
  const { user, token, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (location.state?.question) {
      setInput(location.state.question)
    }
  }, [])

  useEffect(() => {
    setMessages([{
      role: 'assistant',
      content: `Namaste! 👋 I'm Nyay AI, your Indian legal assistant.\n\nI can answer questions about:\n• Tenant & housing rights\n• Consumer complaints\n• Labour laws & minimum wages\n• RTI applications\n• Criminal laws (BNS, BNSS)\n• POCSO, RERA, IT Act, and more\n\nAsk me anything in English or Hindi!`,
      sources: [],
      isWelcome: true
    }])
  }, [])

  const sendMessage = async (text = input) => {
    if (!text.trim() || loading) return
    const question = text.trim()
    setInput('')

    const userMsg = { role: 'user', content: question }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)

    try {
      const endpoint = token ? '/query/ask' : '/query/ask/guest'
      const res = await api.post(endpoint, {
        question,
        language,
        history: history.slice(-6)
      })

      const assistantMsg = {
        role: 'assistant',
        content: res.data.answer,
        sources: res.data.sources || [],
        category: res.data.category
      }

      setMessages(prev => [...prev, assistantMsg])
      setHistory(prev => [...prev, { user: question, assistant: res.data.answer }])
    } catch (err) {
      toast.error('Failed to get answer. Please try again.')
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        sources: [], isError: true
      }])
    } finally {
      setLoading(false)
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []

      mediaRecorderRef.current.ondataavailable = e => audioChunksRef.current.push(e.data)
      mediaRecorderRef.current.onstop = async () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        const formData = new FormData()
        formData.append('audio', blob, 'recording.wav')
        if (language !== 'en') formData.append('language', language)

        try {
          const res = await api.post('/voice/transcribe', formData)
          if (res.data.text) {
            setInput(res.data.text)
            toast.success(`Transcribed: "${res.data.text.substring(0, 40)}..."`)
          }
        } catch {
          toast.error('Transcription failed')
        }
        stream.getTracks().forEach(t => t.stop())
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
      toast.success('Recording... Click again to stop')
    } catch {
      toast.error('Microphone access denied')
    }
  }

  const stopRecording = () => {
    mediaRecorderRef.current?.stop()
    setIsRecording(false)
  }

  const speakAnswer = async (text) => {
    try {
      // Stop any currently playing audio
      if (currentAudioRef.current) {
        currentAudioRef.current.pause()
        currentAudioRef.current = null
      }

      const formData = new FormData()
      formData.append('text', text.substring(0, 500))
      formData.append('language', language)
      const res = await api.post('/voice/speak', formData, { responseType: 'blob' })
      const url = URL.createObjectURL(res.data)
      const audio = new Audio(url)
      currentAudioRef.current = audio
      audio.play()
    } catch {
      toast.error('Text-to-speech failed')
    }
  }

  const popularQuestions = [
    'What are tenant rights under RERA?',
    'How to file consumer complaint?',
    'Minimum wage in India?',
    'RTI application process?'
  ]

  return (
    <div style={{ display: 'flex', height: '100vh', background: '#0a0f1e', overflow: 'hidden' }}>

      {/* Sidebar */}
      <div style={{
        width: '280px', background: '#111827',
        borderRight: '1px solid #1e293b',
        display: 'flex', flexDirection: 'column',
        flexShrink: 0
      }}>
        {/* Logo */}
        <div style={{
          padding: '24px 20px',
          borderBottom: '1px solid #1e293b',
          display: 'flex', alignItems: 'center', gap: '12px'
        }}>
          <div style={{
            width: '36px', height: '36px',
            background: 'linear-gradient(135deg, #c9a84c, #e8c97e)',
            borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            <Scale size={20} color="#0a0f1e" />
          </div>
          <span style={{ fontSize: '18px', fontWeight: '700' }}>
            <span className="gold-text">Nyay AI</span>
          </span>
        </div>

        {/* New Chat */}
        <div style={{ padding: '16px' }}>
          <button
            onClick={() => {
              // Stop any playing audio on new chat
              if (currentAudioRef.current) {
                currentAudioRef.current.pause()
                currentAudioRef.current = null
              }
              setMessages([])
              setHistory([])
              setTimeout(() => setMessages([{
                role: 'assistant',
                content: 'New conversation started! Ask me any legal question.',
                sources: []
              }]), 100)
            }}
            style={{
              width: '100%', padding: '12px 16px',
              background: 'rgba(201,168,76,0.1)',
              border: '1px solid rgba(201,168,76,0.3)',
              borderRadius: '12px', color: '#c9a84c',
              fontWeight: '600', fontSize: '14px', cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: '8px'
            }}>
            <Plus size={18} /> New Chat
          </button>
        </div>

        {/* Language selector */}
        <div style={{ padding: '0 16px 16px' }}>
          <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Language</p>
          <select value={language} onChange={e => setLanguage(e.target.value)}
            style={{
              width: '100%', padding: '10px 12px',
              background: '#0a0f1e', border: '1px solid #2d3748',
              borderRadius: '10px', color: '#f1f5f9', fontSize: '13px'
            }}>
            <option value="en">🇬🇧 English</option>
            <option value="hi">🇮🇳 Hindi</option>
            <option value="ta">Tamil</option>
            <option value="te">Telugu</option>
            <option value="mr">Marathi</option>
            <option value="bn">Bengali</option>
          </select>
        </div>

        {/* Popular Questions */}
        <div style={{ padding: '0 16px', flex: 1 }}>
          <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Quick Questions</p>
          {popularQuestions.map((q, i) => (
            <button key={i} onClick={() => sendMessage(q)}
              style={{
                width: '100%', padding: '10px 12px',
                background: 'transparent', border: 'none',
                borderRadius: '8px', color: '#94a3b8',
                fontSize: '12px', textAlign: 'left', cursor: 'pointer',
                marginBottom: '4px', transition: 'all 0.15s',
                display: 'flex', alignItems: 'center', gap: '8px'
              }}
              onMouseEnter={e => e.currentTarget.style.background = '#1a2235'}
              onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
              <ChevronRight size={12} color="#c9a84c" style={{ flexShrink: 0 }} />
              {q}
            </button>
          ))}
        </div>

        {/* User section */}
        <div style={{
          padding: '16px',
          borderTop: '1px solid #1e293b',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '32px', height: '32px', borderRadius: '50%',
              background: 'linear-gradient(135deg, #c9a84c, #e8c97e)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <User size={16} color="#0a0f1e" />
            </div>
            <span style={{ fontSize: '13px', color: '#94a3b8' }}>
              {user?.name || 'Guest'}
            </span>
          </div>
          {user && (
            <button onClick={() => { logout(); navigate('/') }}
              style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer' }}>
              <LogOut size={16} />
            </button>
          )}
        </div>
      </div>

      {/* Main chat area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '32px 40px' }}>
          {messages.map((msg, i) => (
            <MessageBubble key={i} msg={msg} onSpeak={speakAnswer} />
          ))}
          {loading && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div style={{
          padding: '20px 40px',
          borderTop: '1px solid #1e293b',
          background: '#0a0f1e'
        }}>
          <div style={{
            display: 'flex', gap: '12px', alignItems: 'flex-end',
            background: '#111827',
            border: '1px solid #2d3748',
            borderRadius: '16px', padding: '12px 16px',
            transition: 'border-color 0.2s'
          }}>
            <textarea
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() } }}
              placeholder="Ask a legal question in English or Hindi..."
              rows={1}
              style={{
                flex: 1, background: 'transparent', border: 'none',
                color: '#f1f5f9', fontSize: '15px', resize: 'none',
                outline: 'none', fontFamily: 'Inter, sans-serif',
                lineHeight: '1.5', maxHeight: '120px'
              }}
            />
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <button
                onClick={isRecording ? stopRecording : startRecording}
                style={{
                  width: '38px', height: '38px', borderRadius: '10px',
                  background: isRecording ? 'rgba(239,68,68,0.2)' : 'rgba(201,168,76,0.1)',
                  border: `1px solid ${isRecording ? '#ef4444' : 'rgba(201,168,76,0.3)'}`,
                  color: isRecording ? '#ef4444' : '#c9a84c',
                  cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                {isRecording ? <MicOff size={16} /> : <Mic size={16} />}
              </button>
              <button
                onClick={() => sendMessage()}
                disabled={!input.trim() || loading}
                style={{
                  width: '38px', height: '38px', borderRadius: '10px',
                  background: input.trim() && !loading ? 'linear-gradient(135deg, #c9a84c, #e8c97e)' : '#1e293b',
                  border: 'none',
                  color: input.trim() && !loading ? '#0a0f1e' : '#64748b',
                  cursor: input.trim() && !loading ? 'pointer' : 'not-allowed',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                <Send size={16} />
              </button>
            </div>
          </div>
          <p style={{ fontSize: '11px', color: '#374151', textAlign: 'center', marginTop: '10px' }}>
            Nyay AI provides general legal information, not professional legal advice.
          </p>
        </div>
      </div>
    </div>
  )
}

function MessageBubble({ msg, onSpeak }) {
  const isUser = msg.role === 'user'

  return (
    <div style={{
      display: 'flex',
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: '20px',
      gap: '12px',
      alignItems: 'flex-start'
    }}>
      {!isUser && (
        <div style={{
          width: '32px', height: '32px', borderRadius: '50%',
          background: 'linear-gradient(135deg, #c9a84c, #e8c97e)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0, marginTop: '4px'
        }}>
          <Scale size={16} color="#0a0f1e" />
        </div>
      )}

      <div style={{ maxWidth: '75%' }}>
        <div style={{
          padding: '14px 18px',
          background: isUser
            ? 'linear-gradient(135deg, #c9a84c22, #c9a84c11)'
            : '#1a2235',
          border: `1px solid ${isUser ? 'rgba(201,168,76,0.3)' : '#2d3748'}`,
          borderRadius: isUser ? '18px 4px 18px 18px' : '4px 18px 18px 18px',
          color: '#f1f5f9', fontSize: '15px', lineHeight: '1.7',
          whiteSpace: 'pre-wrap'
        }}>
          {msg.content}
        </div>

        {/* Sources */}
        {!isUser && msg.sources?.length > 0 && (
          <div style={{ marginTop: '10px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {msg.sources.map((s, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', gap: '6px',
                padding: '4px 12px',
                background: 'rgba(59,130,246,0.1)',
                border: '1px solid rgba(59,130,246,0.2)',
                borderRadius: '100px', fontSize: '11px', color: '#93c5fd'
              }}>
                <FileText size={10} />
                {s}
              </div>
            ))}
          </div>
        )}

        {/* Speak button */}
        {!isUser && !msg.isWelcome && (
          <button onClick={() => onSpeak(msg.content)}
            style={{
              marginTop: '8px', padding: '4px 12px',
              background: 'transparent', border: '1px solid #2d3748',
              borderRadius: '100px', color: '#64748b',
              fontSize: '11px', cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: '6px'
            }}>
            <Volume2 size={10} /> Listen
          </button>
        )}
      </div>
    </div>
  )
}

function TypingIndicator() {
  return (
    <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start', marginBottom: '20px' }}>
      <div style={{
        width: '32px', height: '32px', borderRadius: '50%',
        background: 'linear-gradient(135deg, #c9a84c, #e8c97e)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
      }}>
        <Scale size={16} color="#0a0f1e" />
      </div>
      <div style={{
        padding: '14px 18px', background: '#1a2235',
        border: '1px solid #2d3748', borderRadius: '4px 18px 18px 18px',
        display: 'flex', gap: '6px', alignItems: 'center'
      }}>
        {[0, 1, 2].map(i => (
          <div key={i} style={{
            width: '8px', height: '8px', borderRadius: '50%',
            background: '#c9a84c',
            animation: `bounce 1.2s ease-in-out ${i * 0.2}s infinite`
          }} />
        ))}
        <style>{`@keyframes bounce { 0%,80%,100%{transform:scale(0.6);opacity:0.4} 40%{transform:scale(1);opacity:1} }`}</style>
      </div>
    </div>
  )
}