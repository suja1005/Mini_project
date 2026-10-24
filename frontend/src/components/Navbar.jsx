import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { 
  Sparkles, 
  User, 
  LogOut, 
  Bell, 
  HelpCircle, 
  Zap, 
  Menu, 
  X,
  Compass,
  Gift,
  Sun,
  Moon
} from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);

  const getPageTitle = () => {
    const path = location.pathname;
    if (path === '/dashboard') return 'AI Career Guidance';
    if (path === '/profile') return 'Student Profile';
    if (path === '/assessment') return 'Skill Assessment';
    if (path === '/recommendations') return 'Career Recommendations';
    if (path.startsWith('/career')) return 'Career Analysis';
    if (path === '/evidence') return 'Evidence Verification';
    if (path === '/roadmap') return 'Adaptive Roadmap';
    if (path === '/progress') return 'Progress Tracker';
    return 'CareerAI';
  };

  return (
    <>
      <header className="h-15 border-b border-gray-200/80 dark:border-slate-800 bg-white/95 dark:bg-[#0d1322]/95 backdrop-blur-md sticky top-0 z-40 px-4 md:px-6 flex items-center justify-between transition-colors">
        {/* Left: Mobile Toggle & Page Title */}
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-xl text-slate-500 hover:text-slate-800 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800"
            aria-label="Toggle navigation"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

          <div className="flex items-center space-x-3">
            <h1 className="text-base md:text-lg font-bold text-slate-900 dark:text-white tracking-tight flex items-center space-x-2">
              <span>{getPageTitle()}</span>
            </h1>
          </div>
        </div>

        {/* Right Actions: Matching Reference Image */}
        <div className="flex items-center space-x-2.5">
          {/* Upgrade / Pro pill button (matching image black pill) */}
          <Link
            to="/roadmap"
            className="hidden sm:inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 text-white dark:text-slate-900 text-xs font-semibold shadow-xs transition-all active:scale-95"
          >
            <Zap className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
            <span>Phase 2 Pro</span>
          </Link>

          {/* Help circle */}
          <button
            type="button"
            onClick={() => setHelpOpen(!helpOpen)}
            title="Help & Guidance"
            className="p-2 rounded-full text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <HelpCircle className="w-4 h-4" />
          </button>

          {/* Announcements / Gift icon */}
          <button
            type="button"
            title="Latest Updates"
            className="p-2 rounded-full text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors relative"
          >
            <Gift className="w-4 h-4" />
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-600 dark:bg-indigo-400 absolute top-2 right-2 ring-2 ring-white dark:ring-slate-900" />
          </button>

          {/* Mobile Theme Quick Toggle */}
          <button
            type="button"
            onClick={toggleTheme}
            className="md:hidden p-2 rounded-full text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800"
            title="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
          </button>

          {/* User profile avatar pill */}
          <div className="flex items-center space-x-2 pl-2 border-l border-gray-200 dark:border-slate-800">
            <Link
              to="/profile"
              className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold ring-2 ring-indigo-500/20 hover:ring-indigo-500/40 transition-all shadow-xs"
              title="View Profile"
            >
              {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'S'}
            </Link>
          </div>
        </div>
      </header>

      {/* Help Modal */}
      {helpOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/30 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-[#131b2e] w-full max-w-md rounded-2xl shadow-2xl border border-gray-200 dark:border-slate-700 p-6 space-y-4 animate-fade-in">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <HelpCircle className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                <h3 className="text-base font-bold text-slate-900 dark:text-white">Need Guidance?</h3>
              </div>
              <button 
                onClick={() => setHelpOpen(false)}
                className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-lg"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              CareerAI guides you through your career journey in 4 automated steps:
            </p>
            <ol className="text-xs text-slate-600 dark:text-slate-400 space-y-2 list-decimal list-inside bg-slate-50 dark:bg-slate-800/40 p-3 rounded-xl border border-gray-100 dark:border-slate-800">
              <li><strong className="text-slate-900 dark:text-white">Profile & Assessment:</strong> Complete onboarding to calculate baseline score.</li>
              <li><strong className="text-slate-900 dark:text-white">Evidence Engine:</strong> Upload projects, certificates, or GitHub links to earn verified skill badges.</li>
              <li><strong className="text-slate-900 dark:text-white">Adaptive Roadmap:</strong> Take dynamic quizzes and verify milestones to increase employability.</li>
              <li><strong className="text-slate-900 dark:text-white">Progress Analytics:</strong> Track real-time market readiness and employability gap closure.</li>
            </ol>
            <button
              onClick={() => setHelpOpen(false)}
              className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-semibold text-xs shadow-sm transition-all"
            >
              Got it, thanks!
            </button>
          </div>
        </div>
      )}

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs flex">
          <div className="w-64 bg-white dark:bg-[#0d1322] border-r border-gray-200 dark:border-slate-800 p-5 space-y-4 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-900 dark:text-white">CareerAI Menu</span>
                <button onClick={() => setMobileMenuOpen(false)} className="p-1 text-slate-400">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <nav className="space-y-1 text-sm font-medium">
                <Link to="/dashboard" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">AI Chat & Dashboard</Link>
                <Link to="/profile" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">My Profile</Link>
                <Link to="/assessment" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">Assessment</Link>
                <Link to="/recommendations" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">Recommendations</Link>
                <Link to="/evidence" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">Evidence Engine</Link>
                <Link to="/roadmap" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">Adaptive Roadmap</Link>
                <Link to="/progress" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800">Progress Tracker</Link>
              </nav>
            </div>
            <button
              onClick={() => { logout(); setMobileMenuOpen(false); }}
              className="w-full flex items-center justify-center space-x-2 py-2.5 rounded-xl bg-red-50 text-red-600 font-semibold text-xs"
            >
              <LogOut className="w-4 h-4" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Navbar;
