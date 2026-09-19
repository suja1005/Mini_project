import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sparkles, User, LogOut } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="h-16 border-b border-slate-800 bg-[#0f172a]/90 backdrop-blur-md sticky top-0 z-50 px-6 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <Link to="/dashboard" className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-indigo-300">
          CareerAI <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Phase 2</span>
        </Link>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-3 pl-3 border-l border-slate-800">
          <div className="w-9 h-9 rounded-full bg-indigo-900/50 border border-indigo-500/30 flex items-center justify-center text-indigo-300 font-medium">
            <User className="w-5 h-5" />
          </div>
          <div className="hidden sm:block text-left">
            <div className="text-sm font-semibold text-slate-200">{user?.full_name || 'Student'}</div>
            <div className="text-xs text-slate-400">{user?.degree || 'B.Tech'} {user?.department ? `• ${user.department}` : ''}</div>
          </div>
        </div>

        <button 
          onClick={logout}
          title="Sign Out"
          className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-800/80 rounded-lg transition-colors flex items-center space-x-1.5 text-xs font-semibold"
        >
          <LogOut className="w-4 h-4" />
          <span className="hidden md:inline">Logout</span>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
