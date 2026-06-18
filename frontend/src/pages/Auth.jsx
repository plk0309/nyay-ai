import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Scale, Mail, Lock, User, ArrowRight, Eye, EyeOff } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({ name: '', email: '', password: '', preferred_language: 'en' })
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register'
      const payload = isLogin
        ? { email: form.email, password: form.password }
        : form
      const res = await api.post(endpoint, payload)
      login(res.data.user, res.data.token)
      toast.success(isLogin ? 'Welcome back!' : 'Account created!')
      navigate('/chat')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0f1e 0%, #111827 50%, #0a0f1e 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      {/* Background decoration */}
      <div style={{
        position: 'fixed', top: '10%', right: '10%', width: '400px', height: '400px',
        background: 'radial-gradient(circle, rgba(201,168,76,0.06) 0%, transparent 70%)',
        borderRadius: '50%', pointerEvents: 'none'
      }} />

      <div style={{
        background: 'rgba(26,34,53,0.8)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(201,168,76,0.2)',
        borderRadius: '24px',
        padding: '48px',
        width: '100%',
        maxWidth: '440px',
        boxShadow: '0 25px 50px rgba(0,0,0,0.5)'
      }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: '36px' }}>
          <div style={{
            width: '64px', height: '64px',
            background: 'linear-gradient(135deg, #c9a84c, #e8c97e)',
            borderRadius: '16px',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 16px'
          }}>
            <Scale size={32} color="#0a0f1e" />
          </div>
          <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '8px' }}>
            <span className="gold-text">Nyay AI</span>
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '14px' }}>
            {isLogin ? 'Sign in to your account' : 'Create your free account'}
          </p>
        </div>

        {/* Toggle */}
        <div style={{
          display: 'flex',
          background: '#0a0f1e',
          borderRadius: '12px',
          padding: '4px',
          marginBottom: '28px'
        }}>
          {['Login', 'Register'].map((tab, i) => (
            <button key={tab}
              onClick={() => setIsLogin(i === 0)}
              style={{
                flex: 1, padding: '10px',
                borderRadius: '8px', border: 'none',
                background: (isLogin ? i === 0 : i === 1) ? 'linear-gradient(135deg, #c9a84c, #e8c97e)' : 'transparent',
                color: (isLogin ? i === 0 : i === 1) ? '#0a0f1e' : '#94a3b8',
                fontWeight: '600', fontSize: '14px', cursor: 'pointer',
                transition: 'all 0.2s'
              }}>
              {tab}
            </button>
          ))}
        </div>

        {/* Form fields */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {!isLogin && (
            <InputField icon={<User size={16} />} placeholder="Full Name"
              value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
          )}
          <InputField icon={<Mail size={16} />} placeholder="Email address" type="email"
            value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
          <div style={{ position: 'relative' }}>
            <InputField icon={<Lock size={16} />} placeholder="Password"
              type={showPassword ? 'text' : 'password'}
              value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} />
            <button onClick={() => setShowPassword(!showPassword)}
              style={{
                position: 'absolute', right: '16px', top: '50%', transform: 'translateY(-50%)',
                background: 'none', border: 'none', color: '#64748b', cursor: 'pointer'
              }}>
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          </div>

          {!isLogin && (
            <select
              value={form.preferred_language}
              onChange={e => setForm({ ...form, preferred_language: e.target.value })}
              style={{
                background: '#0a0f1e', border: '1px solid #2d3748',
                borderRadius: '12px', padding: '14px 16px',
                color: '#f1f5f9', fontSize: '14px', cursor: 'pointer'
              }}>
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="ta">Tamil</option>
              <option value="te">Telugu</option>
              <option value="mr">Marathi</option>
              <option value="bn">Bengali</option>
            </select>
          )}
        </div>

        {/* Submit */}
        <button onClick={handleSubmit} disabled={loading}
          style={{
            width: '100%', marginTop: '24px', padding: '14px',
            background: loading ? '#2d3748' : 'linear-gradient(135deg, #c9a84c, #e8c97e)',
            border: 'none', borderRadius: '12px',
            color: loading ? '#64748b' : '#0a0f1e',
            fontWeight: '700', fontSize: '16px', cursor: loading ? 'not-allowed' : 'pointer',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
            transition: 'all 0.2s'
          }}>
          {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
          {!loading && <ArrowRight size={18} />}
        </button>

        <p style={{ textAlign: 'center', marginTop: '20px', color: '#64748b', fontSize: '13px' }}>
          By continuing, you agree to our Terms of Service
        </p>
      </div>
    </div>
  )
}

function InputField({ icon, ...props }) {
  return (
    <div style={{ position: 'relative' }}>
      <div style={{
        position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)',
        color: '#64748b'
      }}>{icon}</div>
      <input {...props} style={{
        width: '100%', padding: '14px 16px 14px 44px',
        background: '#0a0f1e', border: '1px solid #2d3748',
        borderRadius: '12px', color: '#f1f5f9', fontSize: '14px',
        outline: 'none', transition: 'border-color 0.2s',
        fontFamily: 'Inter, sans-serif'
      }}
        onFocus={e => e.target.style.borderColor = '#c9a84c'}
        onBlur={e => e.target.style.borderColor = '#2d3748'}
      />
    </div>
  )
}