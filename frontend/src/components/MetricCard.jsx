import React from 'react';

const MetricCard = ({ title, value, subtitle, icon: Icon, color = "indigo" }) => {
  const colorMap = {
    indigo: "from-indigo-500/20 to-purple-500/10 text-indigo-400 border-indigo-500/20",
    emerald: "from-emerald-500/20 to-teal-500/10 text-emerald-400 border-emerald-500/20",
    amber: "from-amber-500/20 to-orange-500/10 text-amber-400 border-amber-500/20",
    cyan: "from-cyan-500/20 to-blue-500/10 text-cyan-400 border-cyan-500/20",
  };

  return (
    <div className="glass-card p-5 rounded-2xl glass-card-hover border border-slate-800 flex items-start justify-between">
      <div>
        <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">
          {title}
        </div>
        <div className="text-2xl font-bold text-white mb-1">
          {value}
        </div>
        {subtitle && (
          <div className="text-xs text-slate-400">
            {subtitle}
          </div>
        )}
      </div>
      {Icon && (
        <div className={`p-3 rounded-xl bg-gradient-to-br ${colorMap[color] || colorMap.indigo} border`}>
          <Icon className="w-6 h-6" />
        </div>
      )}
    </div>
  );
};

export default MetricCard;
