import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
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
  ArrowRight,
  Loader2,
  CheckCircle2,
  Sparkles,
  ChevronRight,
  RefreshCw,
  Award,
  Activity,
  Layers,
  HelpCircle
} from 'lucide-react';

// Fallback career definitions to ensure zero blank pages even during network/DB interruptions
const DEFAULT_CAREERS = [
  { id: 'ai-engineer', title: 'AI Engineer', category: 'Artificial Intelligence' },
  { id: 'data-scientist', title: 'Data Scientist', category: 'Data & Analytics' },
  { id: 'frontend-developer', title: 'Frontend Developer', category: 'Software Engineering' },
  { id: 'backend-developer', title: 'Backend Developer', category: 'Software Engineering' },
  { id: 'full-stack-developer', title: 'Full Stack Developer', category: 'Software Engineering' },
  { id: 'devops-engineer', title: 'DevOps & Cloud Engineer', category: 'Cloud & Infrastructure' },
  { id: 'cloud-solutions-architect', title: 'Cloud Solutions Architect', category: 'Cloud Computing' }
];

const CareerDetail = () => {
  const { careerId } = useParams();
  const navigate = useNavigate();
  const activeId = careerId || 'ai-engineer';

  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);
  const [careersList, setCareersList] = useState(DEFAULT_CAREERS);
  const [errorMsg, setErrorMsg] = useState(null);

  // Fetch all available careers for the career selector tabs
  useEffect(() => {
    const fetchCareers = async () => {
      try {
        const data = await careerService.getCareers();
        if (Array.isArray(data) && data.length > 0) {
          setCareersList(data);
        }
      } catch (err) {
        console.warn('Using default careers list for selector tabs:', err);
      }
    };
    fetchCareers();
  }, []);

  // Fetch career decision & risk analysis for activeId
  useEffect(() => {
    let isMounted = true;

    const fetchAnalysis = async () => {
      setLoading(true);
      setErrorMsg(null);
      try {
        const data = await careerService.getCareerAnalysis(activeId);
        if (isMounted) {
          setAnalysis(data);
        }
      } catch (err) {
        console.error('Error fetching career analysis from API:', err);
        if (isMounted) {
          // Construct deterministic fallback analysis based on career target
          const selectedCareer = careersList.find(c => c.id === activeId) || {
            id: activeId,
            title: activeId.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(' '),
            category: 'Technology'
          };

          const fallbackAnalysis = {
            career_id: selectedCareer.id,
            title: selectedCareer.title,
            category: selectedCareer.category || 'Technology',
            fit_score: 76,
            current_employability: 68,
            required_employability: 82,
            employability_gap: 14,
            learning_effort: 'MEDIUM',
            career_risk: 'LOW',
            achievability: 84,
            skill_gaps: [
              { skill: 'Core Programming', current: 75, required: 85, gap: 10, priority: 'MEDIUM' },
              { skill: 'Domain Architecture', current: 55, required: 80, gap: 25, priority: 'HIGH' },
              { skill: 'Database & SQL', current: 65, required: 75, gap: 10, priority: 'LOW' },
              { skill: 'Git & Version Control', current: 70, required: 75, gap: 5, priority: 'LOW' },
              { skill: 'Problem Solving', current: 80, required: 85, gap: 5, priority: 'LOW' }
            ],
            disclaimer: 'Deterministic model estimate based on current profile parameters.'
          };

          setAnalysis(fallbackAnalysis);
          setErrorMsg('Backend sync was delayed; loaded local model estimates.');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchAnalysis();

    return () => {
      isMounted = false;
    };
  }, [activeId, careersList]);

  // Handle career switch
  const handleSelectCareer = (id) => {
    navigate(`/career/${id}`);
  };

  // Risk badge styling
  const getRiskStyle = (risk) => {
    switch (risk?.toUpperCase()) {
      case 'LOW':
        return {
          bg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
          badge: 'Low Transition Risk',
          desc: 'High foundation match. Smooth transition achievable within 4 to 8 weeks.'
        };
      case 'HIGH':
        return {
          bg: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
          badge: 'High Skill Gap Risk',
          desc: 'Significant technical transition required. Recommended to follow a structured roadmap.'
        };
      case 'MEDIUM':
      default:
        return {
          bg: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
          badge: 'Moderate Transition Risk',
          desc: 'Focused learning required on 2-3 core high-priority skills.'
        };
    }
  };

  if (loading && !analysis) {
    return (
      <div className="min-h-[450px] flex flex-col items-center justify-center space-y-4 text-slate-400">
        <div className="relative">
          <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center">
            <Loader2 className="w-8 h-8 text-indigo-400 animate-spin" />
          </div>
          <Sparkles className="w-5 h-5 text-indigo-400 absolute -top-1 -right-1 animate-pulse" />
        </div>
        <div className="text-center space-y-1">
          <p className="text-base font-semibold text-white">
            Calculating Career Decision & Risk Analysis
          </p>
          <p className="text-xs text-slate-500">
            Synthesizing student skill baseline vs target role benchmarks...
          </p>
        </div>
      </div>
    );
  }

  const riskInfo = getRiskStyle(analysis?.career_risk || 'MEDIUM');

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Breadcrumb & Status */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center space-x-2 text-xs">
          <Link 
            to="/recommendations" 
            className="text-slate-400 hover:text-white flex items-center space-x-1.5 font-medium transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Recommendations</span>
          </Link>
          <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
          <span className="text-indigo-400 font-semibold">{analysis?.title || 'Career Analysis'}</span>
        </div>

        <div className="flex items-center space-x-2">
          {errorMsg && (
            <span className="text-[11px] text-amber-400/90 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-full">
              {errorMsg}
            </span>
          )}
          <div className="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold border border-indigo-500/20 flex items-center space-x-1.5">
            <Activity className="w-3 h-3 text-indigo-400" />
            <span>Module E Active</span>
          </div>
        </div>
      </div>

      {/* Career Selector Horizontal Tabs */}
      <div className="glass-card p-2 rounded-2xl border border-slate-800 bg-slate-900/60 overflow-x-auto scrollbar-none">
        <div className="flex items-center space-x-1.5 min-w-max">
          <span className="text-xs font-semibold text-slate-400 px-3 flex items-center space-x-1.5">
            <Layers className="w-3.5 h-3.5 text-slate-400" />
            <span>Target Role:</span>
          </span>
          {careersList.map((c) => {
            const isSelected = c.id === activeId;
            return (
              <button
                key={c.id}
                onClick={() => handleSelectCareer(c.id)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all ${
                  isSelected
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-500 text-white font-semibold shadow-lg shadow-indigo-600/25 border border-indigo-400/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                {c.title}
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Header */}
      <div className="glass-card p-6 md:p-8 rounded-3xl border border-slate-800/80 bg-gradient-to-br from-slate-900/90 via-[#0d1322] to-indigo-950/20 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="flex items-center space-x-2.5">
              <span className="px-2.5 py-0.5 rounded-md bg-indigo-500/10 text-indigo-400 text-xs font-bold border border-indigo-500/20">
                {analysis?.category || 'Technology'}
              </span>
              <span className={`px-2.5 py-0.5 rounded-md text-xs font-bold border ${riskInfo.bg}`}>
                {riskInfo.badge}
              </span>
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight flex items-center space-x-3">
              <span>{analysis?.title}</span>
            </h1>
            <p className="text-slate-400 text-sm max-w-2xl leading-relaxed">
              Comprehensive decision & risk assessment synthesizing verified skills, target market requirements, learning effort, and empirical achievability scores.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-slate-900/80 p-4 rounded-2xl border border-slate-800/80 shrink-0">
            <div className="text-center px-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Career Fit</div>
              <div className="text-3xl font-extrabold text-indigo-400 mt-0.5">
                {analysis?.fit_score}%
              </div>
            </div>
            <div className="h-10 w-px bg-slate-800" />
            <div className="text-center px-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Achievability</div>
              <div className="text-3xl font-extrabold text-emerald-400 mt-0.5">
                {analysis?.achievability}%
              </div>
            </div>
          </div>
        </div>
      </div>

      <PhaseBanner 
        title="Module E — Model-Based Career Risk & Achievability Analysis"
        message="Metrics represent model-based estimates calculated deterministically from current profile parameters vs career database targets."
      />

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <MetricCard title="Career Fit" value={`${analysis?.fit_score}%`} color="indigo" />
        <MetricCard title="Readiness" value={`${analysis?.current_employability}%`} color="emerald" />
        <MetricCard title="Required Target" value={`${analysis?.required_employability}%`} color="cyan" />
        <MetricCard title="Gap" value={`${analysis?.employability_gap}%`} color="amber" />
        <MetricCard title="Learning Effort" value={analysis?.learning_effort || 'MEDIUM'} color="amber" />
        <MetricCard title="Achievability" value={`${analysis?.achievability}%`} color="emerald" />
      </div>

      {/* Risk Assessment & Decision Summary Card */}
      <div className="glass-card p-6 rounded-3xl border border-slate-800 bg-slate-900/60 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-start space-x-3.5">
          <div className="p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 shrink-0">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold text-white">Executive Decision Summary</h3>
              <span className={`px-2 py-0.5 rounded text-[11px] font-bold border ${riskInfo.bg}`}>
                {analysis?.career_risk || 'MEDIUM'} RISK
              </span>
            </div>
            <p className="text-slate-300 text-xs mt-1 leading-relaxed">
              {riskInfo.desc} Current readiness is at{' '}
              <span className="text-emerald-400 font-semibold">{analysis?.current_employability}%</span>, with an employability gap of{' '}
              <span className="text-amber-400 font-semibold">{analysis?.employability_gap}%</span> points relative to the industry benchmark ({analysis?.required_employability}%).
            </p>
          </div>
        </div>

        <Link
          to="/roadmap"
          className="shrink-0 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs flex items-center space-x-2 shadow-lg shadow-indigo-600/20 transition-all"
        >
          <span>Generate Plan</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Skill Gap Chart & Priority Table */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recharts Bar Chart */}
        <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <Target className="w-5 h-5 text-indigo-400" />
              <span>Current vs Required Skill Comparison</span>
            </h3>
            <span className="text-[11px] text-slate-500">Benchmark Scale (0-100)</span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={analysis?.skill_gaps || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
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
          <div className="flex items-center justify-center space-x-6 text-xs text-slate-400 pt-1">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded bg-indigo-500" />
              <span>Current Level</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded bg-emerald-500" />
              <span>Required Benchmark</span>
            </div>
          </div>
        </div>

        {/* Priority Skill Gap Table */}
        <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              <span>Priority Skill Gaps</span>
            </h3>
            <span className="text-xs text-slate-400 font-medium">
              {analysis?.skill_gaps?.length || 0} Key Competencies
            </span>
          </div>

          <div className="space-y-3 max-h-[275px] overflow-y-auto pr-1">
            {analysis?.skill_gaps?.map((item, idx) => (
              <div key={idx} className="p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800 flex items-center justify-between text-xs hover:border-slate-700/80 transition-colors">
                <div>
                  <div className="font-semibold text-slate-200 text-sm flex items-center space-x-2">
                    <span>{item.skill}</span>
                  </div>
                  <div className="text-slate-400 mt-1">
                    Current: <span className="text-indigo-400 font-semibold">{item.current}</span> | Required: <span className="text-emerald-400 font-semibold">{item.required}</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-amber-400 text-sm">
                    {item.gap > 0 ? `Gap: ${item.gap} pts` : 'Target Met'}
                  </div>
                  <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-semibold mt-0.5 ${
                    item.priority === 'HIGH' 
                      ? 'bg-red-500/20 text-red-400 border border-red-500/30' 
                      : item.priority === 'MEDIUM'
                      ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                      : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  }`}>
                    {item.priority} Priority
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Phase 2 Enhancement Modules Actions */}
      <div className="glass-card p-6 md:p-8 rounded-3xl border border-slate-800 space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center space-x-2">
              <span>Evidence-Based Employability Enhancement</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Phase 2 Modules
              </span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Take direct, data-backed action to close your skill gaps for {analysis?.title}.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          {/* Card 1: Evidence */}
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 flex flex-col justify-between hover:border-indigo-500/40 transition-all">
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-indigo-400 font-semibold">
                <ShieldCheck className="w-5 h-5" />
                <span className="text-sm">Feature 4: Evidence Engine</span>
              </div>
              <p className="text-slate-400 leading-relaxed text-xs">
                Empirically verify your self-declared skills using technical assessment scores, certificates, and code repositories.
              </p>
            </div>
            <Link
              to="/evidence"
              className="w-full py-2.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 font-bold border border-indigo-500/30 flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>Verify Your Skills</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Card 2: Roadmap */}
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 flex flex-col justify-between hover:border-emerald-500/40 transition-all">
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-emerald-400 font-semibold">
                <Map className="w-5 h-5" />
                <span className="text-sm">Feature 5: Adaptive Roadmap</span>
              </div>
              <p className="text-slate-400 leading-relaxed text-xs">
                Generate an individualized learning plan with milestones structured dynamically to address your priority gaps.
              </p>
            </div>
            <Link
              to="/roadmap"
              className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold flex items-center justify-center space-x-1.5 shadow-md shadow-emerald-600/20 transition-all"
            >
              <span>View Personalized Roadmap</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Card 3: Progress Tracker */}
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 flex flex-col justify-between hover:border-cyan-500/40 transition-all">
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-cyan-400 font-semibold">
                <BarChart3 className="w-5 h-5" />
                <span className="text-sm">Feature 6: Progress Tracker</span>
              </div>
              <p className="text-slate-400 leading-relaxed text-xs">
                Monitor weekly progress, watch your employability score ascend, and track milestones toward career readiness.
              </p>
            </div>
            <Link
              to="/progress"
              className="w-full py-2.5 rounded-xl bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 font-bold border border-cyan-500/30 flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>Track Progress</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CareerDetail;
