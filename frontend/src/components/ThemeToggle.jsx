import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const ThemeToggle = ({ className = '' }) => {
  const { theme, setTheme } = useTheme();

  return (
    <div
      className={`inline-flex items-center p-1 rounded-full border border-gray-200/80 bg-gray-100/90 dark:border-slate-800 dark:bg-slate-900/80 transition-colors ${className}`}
      role="group"
      aria-label="Theme toggle"
    >
      <button
        type="button"
        onClick={() => setTheme('light')}
        className={`flex items-center justify-center space-x-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-all duration-200 ${
          theme === 'light'
            ? 'bg-white text-slate-900 shadow-xs border border-gray-200/60'
            : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200'
        }`}
      >
        <Sun className={`w-3.5 h-3.5 ${theme === 'light' ? 'text-amber-500' : ''}`} />
        <span>Light</span>
      </button>

      <button
        type="button"
        onClick={() => setTheme('dark')}
        className={`flex items-center justify-center space-x-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-all duration-200 ${
          theme === 'dark'
            ? 'bg-slate-800 text-white shadow-xs border border-slate-700'
            : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200'
        }`}
      >
        <Moon className={`w-3.5 h-3.5 ${theme === 'dark' ? 'text-indigo-400' : ''}`} />
        <span>Dark</span>
      </button>
    </div>
  );
};

export default ThemeToggle;
