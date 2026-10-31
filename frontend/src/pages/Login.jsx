import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import logo from '../assets/career-guidance-logo.png';
import { Mail, Lock, ArrowRight, AlertCircle, Loader2 } from 'lucide-react';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const from = location.state?.from?.pathname || '/dashboard';

  // If already authenticated, redirect immediately
  if (isAuthenticated) {
    navigate(from, { replace: true });
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await login({ email, password });
      navigate(from, { replace: true });
    } catch (err) {
      console.error("Login error:", err);
      const msg = err.response?.data?.detail || "Invalid email or password. Please try again.";
      setError(msg);
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f5f6f8] dark:bg-[#090d16] flex flex-col items-center justify-center p-4 transition-colors">
      <div className="w-full max-w-md bg-white dark:bg-[#111827] p-8 md:p-10 rounded-3xl border border-gray-200/80 dark:border-slate-800 shadow-sm space-y-6 animate-fade-in">
        <div className="text-center space-y-2">
          <img src={logo} alt="AI Career Guidance" className="auth-brand-logo" />
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Welcome to CareerAI
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Sign in to access your AI guidance & adaptive roadmap
          </p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800/40 text-red-600 dark:text-red-400 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@university.edu"
                className="w-full bg-white dark:bg-slate-800/60 border border-gray-300 dark:border-slate-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-2xs"
                required
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-white dark:bg-slate-800/60 border border-gray-300 dark:border-slate-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-2xs"
                required
              />
            </div>
          </div>

          <button 
            type="submit"
            disabled={submitting}
            className="w-full py-3 rounded-xl bg-slate-900 hover:bg-slate-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold shadow-xs transition-all flex items-center justify-center space-x-2 text-sm disabled:opacity-50 active:scale-98"
          >
            {submitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Signing in...</span>
              </>
            ) : (
              <>
                <span>Sign In to Platform</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="text-center text-xs text-slate-500 dark:text-slate-400 pt-2 border-t border-gray-100 dark:border-slate-800">
          Don't have an account?{' '}
          <Link to="/register" className="text-indigo-600 dark:text-indigo-400 font-bold hover:underline">
            Register Student Account
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
