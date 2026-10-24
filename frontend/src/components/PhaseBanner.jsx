import React from 'react';
import { Sparkles, ShieldCheck } from 'lucide-react';

const PhaseBanner = ({ title, message }) => {
  return (
    <div className="p-4 rounded-2xl bg-indigo-50/80 dark:bg-indigo-950/30 border border-indigo-100 dark:border-indigo-500/30 flex items-start space-x-3.5 text-sm mb-6 transition-colors shadow-xs">
      <div className="p-2 rounded-xl bg-indigo-600 text-white shrink-0 mt-0.5 shadow-xs">
        <ShieldCheck className="w-4 h-4" />
      </div>
      <div className="min-w-0">
        <div className="font-bold text-slate-900 dark:text-indigo-200 flex items-center space-x-2">
          <span>{title}</span>
          <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
            Active
          </span>
        </div>
        <div className="text-slate-600 dark:text-indigo-300/80 text-xs mt-1 leading-relaxed">
          {message}
        </div>
      </div>
    </div>
  );
};

export default PhaseBanner;
