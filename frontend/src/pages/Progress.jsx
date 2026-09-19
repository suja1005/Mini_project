import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { progressService } from '../services/progressService';
import PhaseBanner from '../components/PhaseBanner';
import MetricCard from '../components/MetricCard';
import { 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid 
} from 'recharts';
import { 
  BarChart3, 
  TrendingUp, 
  Target, 
  CheckCircle2, 
  ArrowUpRight, 
  ArrowRight, 
  ShieldCheck, 
  Clock, 
  Loader2,
  Calendar,
  Sparkles
} from 'lucide-react';

const Progress = () => {
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState(null);

  useEffect(() => {
    const fetchProgress = async () => {
      setLoading(true);
      try {
        const data = await progressService.getProgress();
        setOverview(data);
      } catch (err) {
        console.error("Error fetching progress:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProgress();
  }, []);

  if (loading) {
    return (
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Calculating Employability Progress & Skill Trends...</span>
      </div>
    );
  }

  const historyData = overview?.history || [];
  const skillProgress = overview?.skill_progress || [];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center space-x-3">
            <BarChart3 className="w-8 h-8 text-indigo-400" />
            <span>Employability Progress Tracker</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time Longitudinal Skill Evolution & Career Readiness Trajectory
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Link
            to="/roadmap"
            className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs flex items-center space-x-2 shadow-lg shadow-indigo-600/30 transition-all"
          >
            <span>Continue Roadmap</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      <PhaseBanner 
        title="Feature 6 — Longitudinal Employability Progress Tracker"
        message="Tracks verified empirical growth over time. As roadmap tasks are verified, employability scores update dynamically and are logged chronologically."
      />

      {/* Primary Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <MetricCard 
          title="Current Employability" 
          value={`${overview?.current_employability}%`} 
          subtitle={`Previous: ${overview?.previous_employability}%`} 
          icon={TrendingUp} 
          color="emerald" 
        />
        <MetricCard 
          title="Employability Gain" 
          value={overview?.improvement_delta >= 0 ? `+${overview?.improvement_delta}%` : `${overview?.improvement_delta}%`} 
          subtitle="Net Growth from Tasks" 
          icon={ArrowUpRight} 
          color="cyan" 
        />
        <MetricCard 
          title="Target Employability" 
          value={`${overview?.target_employability}%`} 
          subtitle={`Gap: ${overview?.employability_gap}% pts`} 
          icon={Target} 
          color="indigo" 
        />
        <MetricCard 
          title="Tasks Completed" 
          value={`${overview?.completed_tasks_count} / ${overview?.total_tasks_count}`} 
          subtitle={`${overview?.task_completion_rate}% Completion Rate`} 
          icon={CheckCircle2} 
          color="amber" 
        />
      </div>

      {/* Employability History Line Chart */}
      <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <span>Employability Score History</span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Dynamic Timeline
              </span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Longitudinal tracking across assessment milestones and completed roadmap tasks
            </p>
          </div>
          <div className="text-right">
            <span className="text-xs text-slate-400 font-semibold">Target Benchmark: </span>
            <span className="text-xs text-indigo-400 font-bold">{overview?.target_employability}%</span>
          </div>
        </div>

        <div className="h-72 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={historyData} margin={{ top: 15, right: 20, left: -15, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="date" stroke="#94a3b8" tick={{ fontSize: 11 }} />
              <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} domain={[30, 100]} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '14px', fontSize: '12px' }}
                formatter={(value) => [`${value}%`, 'Employability Score']}
                labelFormatter={(label, payload) => {
                  const milestone = payload?.[0]?.payload?.milestone;
                  return `${label} — ${milestone || ''}`;
                }}
              />
              <Line 
                type="monotone" 
                dataKey="score" 
                stroke="#10b981" 
                strokeWidth={3} 
                dot={{ r: 5, fill: '#10b981', stroke: '#0f172a', strokeWidth: 2 }}
                activeDot={{ r: 8, fill: '#6366f1' }}
                name="Employability"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Skill Progress & Evidence Status Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Skill Progress Bars (Left 2 cols) */}
        <div className="lg:col-span-2 glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <Target className="w-5 h-5 text-indigo-400" />
                <span>Skill Progression & Target Alignment</span>
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Current verified competency vs target requirements for {overview?.target_career}
              </p>
            </div>
            <Link to="/evidence" className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center space-x-1">
              <span>View Evidence</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-4 pt-2">
            {skillProgress.map((item) => {
              const isAchieved = item.gap === 0;
              const hasImproved = item.improvement > 0;

              return (
                <div key={item.skill} className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2.5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-sm text-white">{item.skill}</span>
                      {isAchieved ? (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                          Target Achieved ✓
                        </span>
                      ) : (
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          hasImproved 
                            ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' 
                            : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        }`}>
                          {hasImproved ? `+${item.improvement} pts gain` : 'Needs Action'}
                        </span>
                      )}
                    </div>

                    <div className="text-right text-xs">
                      <span className="text-slate-400">Current: </span>
                      <span className="text-indigo-400 font-bold">{item.current_score}</span>
                      <span className="text-slate-500"> / Target: </span>
                      <span className="text-emerald-400 font-bold">{item.target_score}</span>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="space-y-1">
                    <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${
                          isAchieved ? 'bg-emerald-400' : 'bg-gradient-to-r from-indigo-500 to-emerald-400'
                        }`}
                        style={{ width: `${Math.min(100, (item.current_score / item.target_score) * 100)}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-[11px] text-slate-500">
                      <span>Baseline: {item.initial_score} pts</span>
                      <span>Remaining Gap: {item.gap} pts</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Evidence Status & Milestone Timeline (Right 1 col) */}
        <div className="space-y-6">
          {/* Verification Status Summary */}
          <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-indigo-400" />
              <span>Evidence Engine Health</span>
            </h3>

            <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Fully Verified Skills:</span>
                <span className="font-bold text-emerald-400 text-sm">{overview?.verified_skills_count}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Partially Verified:</span>
                <span className="font-bold text-amber-400 text-sm">{overview?.partial_skills_count}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Overall Verification:</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  {overview?.verified_skills_count >= 3 ? 'Active & Robust' : 'Building Evidence'}
                </span>
              </div>
            </div>

            <div className="pt-1">
              <Link 
                to="/evidence"
                className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs flex items-center justify-center space-x-1.5 transition-all"
              >
                <span>Manage Evidence Artifacts</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>

          {/* Timeline Milestones */}
          <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <Calendar className="w-5 h-5 text-indigo-400" />
              <span>Milestone Log</span>
            </h3>

            <div className="space-y-3">
              {historyData.slice(-4).reverse().map((h, i) => (
                <div key={i} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs flex items-center justify-between">
                  <div>
                    <div className="font-semibold text-white">{h.milestone}</div>
                    <div className="text-slate-500 text-[10px] mt-0.5">{h.date}</div>
                  </div>
                  <span className="font-bold text-emerald-400 text-sm">
                    {h.score}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Progress;
