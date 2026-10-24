import React from 'react';

const MetricCard = ({ title, value, subtitle, icon: Icon, color = "indigo", badge = null }) => {
  const badgeColors = {
    indigo: "bg-indigo-50 text-indigo-700 border-indigo-100 dark:bg-indigo-950/40 dark:text-indigo-400 dark:border-indigo-800/40",
    emerald: "bg-emerald-50 text-emerald-700 border-emerald-100 dark:bg-emerald-950/40 dark:text-emerald-400 dark:border-emerald-800/40",
    amber: "bg-amber-50 text-amber-700 border-amber-100 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800/40",
    cyan: "bg-cyan-50 text-cyan-700 border-cyan-100 dark:bg-cyan-950/40 dark:text-cyan-400 dark:border-cyan-800/40",
    purple: "bg-purple-50 text-purple-700 border-purple-100 dark:bg-purple-950/40 dark:text-purple-400 dark:border-purple-800/40",
  };

  return (
    <div className="bg-white dark:bg-[#131b2e] p-5 rounded-2xl border border-gray-200/80 dark:border-slate-800 shadow-xs hover:shadow-md dark:hover:border-indigo-500/30 transition-all duration-200 flex items-start justify-between group">
      <div className="space-y-1.5">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
            {title}
          </span>
          {badge && (
            <span className={`text-[10px] font-bold px-1.5 py-0.2 rounded-full border ${badgeColors[color] || badgeColors.indigo}`}>
              {badge}
            </span>
          )}
        </div>
        <div className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          {value}
        </div>
        {subtitle && (
          <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">
            {subtitle}
          </div>
        )}
      </div>

      {Icon && (
        <div className={`p-3 rounded-xl border ${badgeColors[color] || badgeColors.indigo} transition-transform group-hover:scale-105 shrink-0`}>
          <Icon className="w-5 h-5" />
        </div>
      )}
    </div>
  );
};

export default MetricCard;
