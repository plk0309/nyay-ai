import { useNavigate } from 'react-router-dom'
import { Scale, MessageSquare, Mic, FileText, Shield, Zap, Globe, ChevronRight } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Home() {
  const navigate = useNavigate()
  const { user } = useAuth()

  const features = [
    { icon: <MessageSquare size={24} />, title: 'Ask Legal Questions', desc: 'Get instant answers based on actual Indian laws and acts' },
    { icon: <Mic size={24} />, title: 'Voice Input', desc: 'Speak your query in Hindi or English — we understand both' },
    { icon: <FileText size={24} />, title: 'Source Citations', desc: 'Every answer cites the exact law and section number' },
    { icon: <Globe size={24} />, title: 'Vernacular Support', desc: 'Available in Hindi, Tamil, Telugu, Marathi and more' },
    { icon: <Shield size={24} />, title: 'Privacy First', desc: 'Your conversations are secure and never shared' },
    { icon: <Zap size={24} />, title: 'Instant Answers', desc: 'Powered by RAG — retrieval from verified legal documents' },
  ]

  const popularQuestions = [
    'What are my rights as a tenant?',
    'How to file a consumer complaint?',
    'What does POCSO protect?',
    'How to apply for RTI?',
  ]

  return (
    <div style={{ minHeight: '100vh', background: '#0a0f1e' }}>
      {/* Navbar */}
      <nav style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '20px 60px',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
        position: 'sticky', top: 0, zIndex: 100,
        background: 'rgba(10,15,30,0.9)', backdropFilter: 'blur(20px)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px', height: '40px',
            background: 'linear-gradient(135deg, #c9a84c, #e8c97e)',
            borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            <Scale size={22} color="#0a0f1e" />
          </div>
          <span style={{ fontSize: '22px', fontWeight: '700' }}>
            <span className="gold-text">Nyay AI</span>
          </span>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          {user ? (
            <button onClick={() => navigate('/chat')}
              style={btnStyle('gold')}>
              Go to Chat <ChevronRight size={16} />
            </button>
          ) : (
            <>
              <button onClick={() => navigate('/auth')} style={btnStyle('ghost')}>Sign In</button>
              <button onClick={() => navigate('/auth')} style={btnStyle('gold')}>Get Started</button>
            </>
          )}
        </div>
      </nav>

      {/* Hero */}
      <section style={{
        textAlign: 'center', padding: '100px 60px 80px',
        position: 'relative', overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute', top: '0', left: '50%', transform: 'translateX(-50%)',
          width: '800px', height: '400px',
          background: 'radial-gradient(ellipse, rgba(201,168,76,0.08) 0%, transparent 70%)',
          pointerEvents: 'none'
        }} />

        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: '8px',
          background: 'rgba(201,168,76,0.1)', border: '1px solid rgba(201,168,76,0.3)',
          borderRadius: '100px', padding: '6px 16px', marginBottom: '24px'
        }}>
          <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#10b981' }} />
          <span style={{ fontSize: '13px', color: '#c9a84c', fontWeight: '500' }}>
            Powered by RAG + Indian Legal Documents
          </span>
        </div>

        <h1 style={{
          fontSize: '64px', fontWeight: '700', lineHeight: '1.1',
          marginBottom: '24px', maxWidth: '800px', margin: '0 auto 24px'
        }}>
          Legal Help in Your <br />
          <span className="gold-text">Own Language</span>
        </h1>

        <p style={{
          fontSize: '20px', color: '#94a3b8', maxWidth: '560px',
          margin: '0 auto 48px', lineHeight: '1.6'
        }}>
          Ask any question about Indian law. Get clear, source-backed answers instantly — in Hindi, English, or your regional language.
        </p>

        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button onClick={() => navigate(user ? '/chat' : '/auth')}
            style={{
              padding: '16px 36px',
              background: 'linear-gradient(135deg, #c9a84c, #e8c97e)',
              border: 'none', borderRadius: '14px',
              color: '#0a0f1e', fontWeight: '700', fontSize: '16px',
              cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px'
            }}>
            Start Asking Free <ChevronRight size={18} />
          </button>
          <button onClick={() => navigate('/chat')}
            style={{
              padding: '16px 36px',
              background: 'transparent',
              border: '1px solid #2d3748', borderRadius: '14px',
              color: '#f1f5f9', fontWeight: '600', fontSize: '16px',
              cursor: 'pointer'
            }}>
            Try as Guest
          </button>
        </div>

        {/* Popular questions */}
        <div style={{ marginTop: '64px' }}>
          <p style={{ color: '#64748b', fontSize: '13px', marginBottom: '16px' }}>POPULAR QUESTIONS</p>
          <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
            {popularQuestions.map(q => (
              <button key={q}
                onClick={() => navigate('/chat', { state: { question: q } })}
                style={{
                  padding: '10px 20px',
                  background: 'rgba(26,34,53,0.8)',
                  border: '1px solid #2d3748', borderRadius: '100px',
                  color: '#94a3b8', fontSize: '13px', cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={e => { e.target.style.borderColor = '#c9a84c'; e.target.style.color = '#c9a84c' }}
                onMouseLeave={e => { e.target.style.borderColor = '#2d3748'; e.target.style.color = '#94a3b8' }}>
                {q}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section style={{ padding: '80px 60px', maxWidth: '1200px', margin: '0 auto' }}>
        <h2 style={{ textAlign: 'center', fontSize: '40px', fontWeight: '700', marginBottom: '60px' }}>
          Why <span className="gold-text">Nyay AI?</span>
        </h2>
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px'
        }}>
          {features.map((f, i) => (
            <div key={i} style={{
              background: '#1a2235', border: '1px solid #1e293b',
              borderRadius: '16px', padding: '28px',
              transition: 'all 0.2s', cursor: 'default'
            }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(201,168,76,0.3)'; e.currentTarget.style.transform = 'translateY(-4px)' }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = '#1e293b'; e.currentTarget.style.transform = 'translateY(0)' }}>
              <div style={{
                width: '48px', height: '48px',
                background: 'rgba(201,168,76,0.1)', borderRadius: '12px',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: '#c9a84c', marginBottom: '16px'
              }}>
                {f.icon}
              </div>
              <h3 style={{ fontSize: '17px', fontWeight: '600', marginBottom: '8px' }}>{f.title}</h3>
              <p style={{ fontSize: '14px', color: '#64748b', lineHeight: '1.6' }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid #1e293b', padding: '32px 60px',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        color: '#64748b', fontSize: '13px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Scale size={16} color="#c9a84c" />
          <span>Nyay AI — Legal Aid for Everyone</span>
        </div>
        <span>Built with RAG · Indian Laws · Vernacular NLP</span>
      </footer>
    </div>
  )
}

function btnStyle(type) {
  if (type === 'gold') return {
    padding: '10px 24px',
    background: 'linear-gradient(135deg, #c9a84c, #e8c97e)',
    border: 'none', borderRadius: '10px',
    color: '#0a0f1e', fontWeight: '600', fontSize: '14px',
    cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px'
  }
  return {
    padding: '10px 24px',
    background: 'transparent',
    border: '1px solid #2d3748', borderRadius: '10px',
    color: '#94a3b8', fontWeight: '600', fontSize: '14px',
    cursor: 'pointer'
  }
}