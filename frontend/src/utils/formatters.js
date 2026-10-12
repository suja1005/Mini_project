/**
 * Utility functions for formatting scores, percentages, and metrics.
 */

export const formatPercent = (val) => {
  if (val === null || val === undefined) return '0%';
  return `${Math.round(val)}%`;
};

export const getScoreBadgeColor = (score) => {
  if (score >= 80) return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
  if (score >= 60) return 'text-indigo-400 bg-indigo-500/10 border-indigo-500/30';
  if (score >= 40) return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
  return 'text-rose-400 bg-rose-500/10 border-rose-500/30';
};

export const getEffortBadgeColor = (effort) => {
  switch (String(effort).toLowerCase()) {
    case 'low':
      return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
    case 'medium':
      return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
    case 'high':
      return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
    default:
      return 'text-slate-400 bg-slate-500/10 border-slate-500/20';
  }
};
