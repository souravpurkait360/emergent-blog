import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import { toast } from 'sonner';
import { Eye, EyeOff } from 'lucide-react';

export default function Auth() {
  const [tab, setTab] = useState('login');
  const [form, setForm] = useState({ email: '', password: '', username: '', first_name: '', last_name: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const update = (k, v) => setForm(prev => ({ ...prev, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (tab === 'login') {
        await login(form.email, form.password);
        toast.success('Welcome back!');
      } else {
        await register(form);
        toast.success('Account created!');
      }
      navigate('/');
    } catch (e) {
      const detail = e.response?.data;
      if (typeof detail === 'object' && !Array.isArray(detail)) {
        setError(Object.values(detail).flat().join(' '));
      } else {
        setError(e.response?.data?.detail || 'Something went wrong');
      }
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-6 py-16 bg-[#FDFDFD]">
      <motion.div
        initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md border border-[#E4E4E7] bg-white p-10"
        data-testid="auth-container"
      >
        <h1 className="text-3xl font-black tracking-tight mb-2 text-[#050505]" style={{fontFamily:"'Outfit',sans-serif"}}>
          {tab === 'login' ? 'Welcome back' : 'Create account'}
        </h1>
        <p className="text-sm text-[#52525B] mb-8">
          {tab === 'login' ? "Don't have an account? " : "Already have an account? "}
          <button onClick={() => { setTab(tab === 'login' ? 'register' : 'login'); setError(''); }}
            className="text-[#002FA7] underline" data-testid="toggle-auth-btn">
            {tab === 'login' ? 'Register' : 'Login'}
          </button>
        </p>

        {error && <p className="text-sm text-red-600 bg-red-50 p-3 mb-4 border border-red-200" data-testid="auth-error">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          {tab === 'register' && (
            <div className="grid grid-cols-2 gap-3">
              <input value={form.first_name} onChange={e => update('first_name', e.target.value)}
                placeholder="First name" className="border border-[#E4E4E7] p-4 text-sm focus:ring-2 focus:ring-[#002FA7] outline-none" data-testid="first-name-input" />
              <input value={form.last_name} onChange={e => update('last_name', e.target.value)}
                placeholder="Last name" className="border border-[#E4E4E7] p-4 text-sm focus:ring-2 focus:ring-[#002FA7] outline-none" data-testid="last-name-input" />
            </div>
          )}
          <input value={form.email} onChange={e => update('email', e.target.value)}
            type="email" placeholder="Email address" required
            className="w-full border border-[#E4E4E7] p-4 text-sm focus:ring-2 focus:ring-[#002FA7] outline-none"
            data-testid="email-input" />
          <div className="relative">
            <input value={form.password} onChange={e => update('password', e.target.value)}
              type={showPassword ? 'text' : 'password'} placeholder="Password" required minLength={6}
              className="w-full border border-[#E4E4E7] p-4 text-sm focus:ring-2 focus:ring-[#002FA7] outline-none pr-12"
              data-testid="password-input" />
            <button type="button" onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-[#A1A1AA]">
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          </div>
          <button type="submit" disabled={loading}
            className="w-full bg-[#002FA7] text-white py-4 text-sm font-medium hover:bg-[#002280] transition-colors disabled:opacity-50"
            data-testid="auth-submit-btn">
            {loading ? 'Please wait...' : tab === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </form>
      </motion.div>
    </div>
  );
}
