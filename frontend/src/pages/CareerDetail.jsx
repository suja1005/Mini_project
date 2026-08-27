import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { careerService } from '../services/careerService';
import PhaseBanner from '../components/PhaseBanner';
import MetricCard from '../components/MetricCard';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { 
  TrendingUp, 
  Target, 
  AlertTriangle, 
  ShieldCheck, 
  Map, 
  BarChart3,
  ArrowLeft,
  Loader2
} from 'lucide-react';

const CareerDetail = () => {
  const { careerId } = useParams();
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      setLoading(true);
      try {
        const data = await careerService.getCareerAnalysis(careerId || 'ai-engineer');
        setAnalysis(data);
      } catch (err) {
        console.error("Error fetching career analysis:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalysis();
  }, [careerId]);

  if (loading) {
    return (
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Calculating Career Decision & Risk Analysis for {careerId}...</span>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="p-8 text-center text-slate-400 space-y-4">
        <p>Career profile not found.</p>
        <Link to="/recommendations" className="text-indigo-400 underline">Back to Recommendations</Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Top Navigation */}
      <div className="flex items-center justify-between">
        <Link to="/recommendations" className="text-xs text-slate-400 hover:text-white flex items-center space-x-1.5 font-medium">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Recommendations</span>
        </Link>
        <div className="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold border border-indigo-500/20">
          Module E Connected
        </div>
      </div>

      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white">
            {analysis.title} <span className="text-slate-500 text-lg font-medium">Decision & Risk Analysis</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Model-based estimate of fit, skill gaps, learning effort, and overall achievability score.
          </p>
        </div>
        <div className="px-4 py-2 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-300 font-bold text-lg">
          Career Fit: {analysis.fit_score}%
        </div>
      </div>

      <PhaseBanner 
        title="Module E — Model-Based Career Risk & Achievability Estimate"
        message="Metrics represent model-based estimates calculated deterministically from current profile parameters vs career database targets."
      />

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <MetricCard title="Career Fit" value={`${analysis.fit_score}%`} color="indigo" />
        <MetricCard title="Readiness" value={`${analysis.current_employability}%`} color="emerald" />
        <MetricCard title="Required Target" value={`${analysis.required_employability}%`} color="cyan" />
        <MetricCard title="Gap" value={`${analysis.employability_gap}%`} color="amber" />
        <MetricCard title="Learning Effort" value={analysis.learning_effort} color="amber" />
        <MetricCard title="Achievability" value={`${analysis.achievability}%`} color="emerald" />
      </div>

      {/* Skill Gap Chart & Priority Table */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recharts Bar Chart */}
        <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <Target className="w-5 h-5 text-indigo-400" />
            <span>Current vs Required Skill Comparison</span>
          </h3>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={analysis.skill_gaps} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="skill" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} domain={[0, 100]} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                />
                <Bar dataKey="current" fill="#6366f1" radius={[4, 4, 0, 0]} name="Current Level" />
                <Bar dataKey="required" fill="#10b981" radius={[4, 4, 0, 0]} name="Required Level" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Priority Skill Gap Table */}
        <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <span>Priority Skill Gaps</span>
          </h3>

          <div className="space-y-3">
            {analysis.skill_gaps.map((item, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between text-xs">
                <div>
                  <div className="font-semibold text-slate-200 text-sm">{item.skill}</div>
                  <div className="text-slate-400 mt-0.5">
                    Current: <span className="text-indigo-400 font-semibold">{item.current}</span> | Required: <span className="text-emerald-400 font-semibold">{item.required}</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-amber-400 text-sm">Gap: {item.gap} pts</div>
                  <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-semibold mt-0.5 ${
                    item.priority === 'HIGH' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  }`}>
                    {item.priority} Priority
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Architecture Placeholders for Future Modules */}
      <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-slate-300">Upcoming System Modules (Phases 2 & 3)</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-2 opacity-75">
            <div className="flex items-center space-x-2 text-slate-400 font-semibold">
              <ShieldCheck className="w-4 h-4 text-slate-500" />
              <span>Feature 4: Evidence Engine</span>
            </div>
            <p className="text-slate-500">
              Evidence verification will be available in the next phase.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-2 opacity-75">
            <div className="flex items-center space-x-2 text-slate-400 font-semibold">
              <Map className="w-4 h-4 text-slate-500" />
              <span>Feature 5: Adaptive Roadmap</span>
            </div>
            <p className="text-slate-500">
              Personalized roadmap will be generated after skill-gap verification.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-2 opacity-75">
            <div className="flex items-center space-x-2 text-slate-400 font-semibold">
              <BarChart3 className="w-4 h-4 text-slate-500" />
              <span>Feature 6: Progress Tracker</span>
            </div>
            <p className="text-slate-500">
              Employability progress tracking will become available after roadmap activities are completed.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CareerDetail;
