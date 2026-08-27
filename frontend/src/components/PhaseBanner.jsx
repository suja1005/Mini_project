import React from 'react';
import { Info } from 'lucide-react';

const PhaseBanner = ({ title, message }) => {
  return (
    <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/30 flex items-start space-x-3 text-sm mb-6">
      <Info className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
      <div>
        <div className="font-semibold text-indigo-200">{title}</div>
        <div className="text-indigo-300/80 text-xs mt-0.5">{message}</div>
      </div>
    </div>
  );
};

export default PhaseBanner;
