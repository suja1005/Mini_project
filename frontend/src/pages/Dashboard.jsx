import React, { useEffect, useState, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { roadmapService } from '../services/roadmapService';
import {
  BookOpen,
  CheckCircle2,
  Clock,
  Lock,
  Unlock,
  Award,
  TrendingUp,
  Map,
  ArrowRight,
  Loader2,
  AlertCircle,
  Sparkles,
  Play,
  ClipboardCheck,
  RotateCcw,
  ChevronRight,
  Target,
  Star,
  Zap,
  BarChart3,
  CheckSquare,
  Circle,
  Activity
} from 'lucide-react';
import ChatbotWidget from '../components/ChatbotWidget';

// ─────────────────────────────────────────────
// Colour tokens (violet-first, white background)
// ─────────────────────────────────────────────
const violet = {
  600: '#7C3AED',
  700: '#6D28D9',
  100: '#EDE9FE',
  50:  '#F5F3FF',
};

// Helper: format ISO timestamp to friendly relative string
function timeAgo(isoStr) {
  if (!isoStr) return '';
  try {
    const diff = Date.now() - new Date(isoStr).getTime();
    const mins  = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days  = Math.floor(diff / 86400000);
    if (mins  < 2)  return 'just now';
    if (mins  < 60) return `${mins}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days  < 30) return `${days}d ago`;
    return new Date(isoStr).toLocaleDateString();
  } catch {
    return '';
  }
}

// ─────────────────────────────────────────────
// Stat Card (used in "My Learning Activity")
// ─────────────────────────────────────────────
const StatCard = ({ icon: Icon, label, value, color = 'violet', bg }) => {
  const colorMap = {
    violet: { text: 'text-violet-600', bg: 'bg-violet-50', border: 'border-violet-100' },
    green:  { text: 'text-green-600',  bg: 'bg-green-50',  border: 'border-green-100'  },
    orange: { text: 'text-orange-500', bg: 'bg-orange-50', border: 'border-orange-100' },
    gray:   { text: 'text-slate-500',  bg: 'bg-slate-50',  border: 'border-slate-200'  },
    blue:   { text: 'text-blue-600',   bg: 'bg-blue-50',   border: 'border-blue-100'   },
  };
  const c = colorMap[color] || colorMap.violet;
  return (
    <div className={`p-4 rounded-2xl border ${c.border} ${bg || c.bg} flex flex-col gap-2`}>
      <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${c.bg} ${c.text}`}>
        <Icon className="w-5 h-5" />
      </div>
      <div className={`text-2xl font-black ${c.text}`}>{value ?? '—'}</div>
      <div className="text-xs font-semibold text-slate-500 leading-tight">{label}</div>
    </div>
  );
};

// ─────────────────────────────────────────────
// Phase Status Badge
// ─────────────────────────────────────────────
const PhaseBadge = ({ status }) => {
  if (status === 'COMPLETED') return (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-green-100 text-green-700 border border-green-200">
      <CheckCircle2 className="w-3 h-3" /> Completed
    </span>
  );
  if (status === 'LOCKED') return (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-500 border border-slate-200">
      <Lock className="w-3 h-3" /> Locked
    </span>
  );
  // AVAILABLE / IN_PROGRESS
  return (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-violet-100 text-violet-700 border border-violet-200">
      <Unlock className="w-3 h-3" /> Unlocked
    </span>
  );
};

// ─────────────────────────────────────────────
// Phase Card
// ─────────────────────────────────────────────
const PhaseCard = ({ phase, index }) => {
  if (!phase) return null;
  const isCompleted = phase.status === 'COMPLETED';
  const isLocked    = phase.status === 'LOCKED';
  const isActive    = !isCompleted && !isLocked;

  const borderCls = isCompleted
    ? 'border-green-200'
    : isActive
    ? 'border-violet-200 shadow-sm shadow-violet-100'
    : 'border-slate-200 opacity-75';

  const bgCls = isCompleted
    ? 'bg-green-50/40'
    : isActive
    ? 'bg-violet-50/30'
    : 'bg-slate-50/50';

  const phaseLabels = ['Beginner', 'Intermediate', 'Advanced'];
  const phaseIcons  = [BookOpen, TrendingUp, Star];
  const PhaseIcon   = phaseIcons[index] || BookOpen;

  return (
    <div className={`p-5 rounded-2xl border ${borderCls} ${bgCls} flex flex-col gap-3`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center
            ${isCompleted ? 'bg-green-100 text-green-600' :
              isActive    ? 'bg-violet-100 text-violet-600' :
                            'bg-slate-100 text-slate-400'}`}>
            <PhaseIcon className="w-4 h-4" />
          </div>
          <div>
            <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Phase {index + 1}
            </div>
            <div className="text-sm font-bold text-slate-800">{phase.name}</div>
          </div>
        </div>
        <PhaseBadge status={phase.status} />
      </div>

      {/* Progress bar */}
      <div>
        <div className="flex justify-between text-[11px] font-semibold text-slate-500 mb-1">
          <span>{phase.completed_topics_count}/{phase.total_topics_count} Topics</span>
          <span>{phase.progress_percentage}%</span>
        </div>
        <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-700 ${
              isCompleted ? 'bg-green-500' : isActive ? 'bg-violet-500' : 'bg-slate-300'
            }`}
            style={{ width: `${phase.progress_percentage}%` }}
          />
        </div>
      </div>

      {/* Score */}
      <div className="text-[11px] text-slate-500 flex items-center justify-between">
        <span>Best Assessment Score</span>
        <span className={`font-bold ${
          phase.best_score >= 80 ? 'text-green-600' :
          phase.best_score !== null && phase.best_score !== undefined ? 'text-orange-500' :
          'text-slate-400'
        }`}>
          {phase.best_score !== null && phase.best_score !== undefined
            ? `${phase.best_score}%`
            : 'Not taken'}
        </span>
      </div>

      {/* Locked reason */}
      {isLocked && (
        <div className="text-[10px] text-slate-400 italic flex items-center gap-1 pt-1 border-t border-slate-200/60">
          <Lock className="w-3 h-3 shrink-0" />
          Pass previous phase assessment (≥80%) to unlock
        </div>
      )}
    </div>
  );
};

// ─────────────────────────────────────────────
// Activity Item
// ─────────────────────────────────────────────
const ActivityItem = ({ activity }) => {
  const isGreen  = activity.color === 'green';
  const isOrange = activity.color === 'orange';

  return (
    <div className="flex items-start gap-3 py-2.5">
      <div className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5
        ${isGreen ? 'bg-green-100 text-green-600' :
          isOrange ? 'bg-orange-100 text-orange-500' :
                     'bg-violet-100 text-violet-600'}`}>
        {activity.icon === 'check'    && <CheckCircle2 className="w-3.5 h-3.5" />}
        {activity.icon === 'award'    && <Award className="w-3.5 h-3.5" />}
        {activity.icon === 'x-circle' && <RotateCcw className="w-3.5 h-3.5" />}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-semibold text-slate-800 truncate">{activity.title}</p>
        <p className="text-[11px] text-slate-500 truncate">{activity.description}</p>
      </div>
      {activity.timestamp && (
        <span className="text-[10px] text-slate-400 shrink-0 pt-0.5">
          {timeAgo(activity.timestamp)}
        </span>
      )}
    </div>
  );
};

// ─────────────────────────────────────────────
// MAIN DASHBOARD COMPONENT
// ─────────────────────────────────────────────
const Dashboard = () => {
  const { user } = useAuth();
  const navigate  = useNavigate();

  const [summary,  setSummary]  = useState(null);
  const [activity, setActivity] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [summaryRes, activityRes] = await Promise.allSettled([
        roadmapService.getDashboardSummary(),
        roadmapService.getRecentActivity(),
      ]);
      if (summaryRes.status === 'fulfilled')  setSummary(summaryRes.value);
      if (activityRes.status === 'fulfilled') setActivity(activityRes.value || []);
    } catch (err) {
      console.error('Dashboard fetch error:', err);
      setError('Failed to load dashboard data. Please refresh.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  // ── Derived helpers ──────────────────────────────────────────────────────────
  const studentName = summary?.student_name
    || user?.full_name
    || 'Student';

  const firstName = studentName.split(' ')[0];

  const phases = summary?.phases || [];
  const beginnerPhase      = phases[0];
  const intermediatePhase  = phases[1];
  const advancedPhase      = phases[2];

  // Assessment eligibility: any unlocked phase with all topics done and not yet passed
  const eligibleAssessmentPhase = phases.find(
    p => p.assessment_eligible && p.status !== 'COMPLETED'
  );

  // ── Loading state ─────────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-8 h-8 text-violet-600 animate-spin" />
        <p className="text-sm font-medium text-slate-500">Loading your dashboard…</p>
      </div>
    );
  }

  // ── Error state ───────────────────────────────────────────────────────────────
  if (error) {
    return (
      <div className="min-h-[40vh] flex flex-col items-center justify-center gap-4">
        <AlertCircle className="w-10 h-10 text-red-400" />
        <p className="text-sm text-slate-600">{error}</p>
        <button
          onClick={fetchData}
          className="px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-semibold hover:bg-violet-700 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  // ── Main render ───────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-white pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        {/* ================================================================== */}
        {/* A. PERSONALIZED WELCOME SECTION                                     */}
        {/* ================================================================== */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 md:p-8 shadow-sm
                        flex flex-col sm:flex-row sm:items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            {/* Avatar / Greeting Icon */}
            <div className="w-14 h-14 rounded-2xl bg-violet-600 flex items-center justify-center shrink-0 shadow-sm">
              <span className="text-2xl font-black text-white">
                {firstName.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-black text-slate-900 tracking-tight">
                Welcome back, <span className="text-violet-600">{firstName}!</span>
              </h1>
              <p className="text-slate-500 text-sm mt-0.5">
                Continue your learning journey and improve your employability.
              </p>
            </div>
          </div>

          {/* Quick navigation shortcut */}
          <Link
            to="/roadmap"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-violet-600
                       hover:bg-violet-700 text-white text-sm font-bold transition-colors shadow-sm shrink-0"
          >
            <Play className="w-4 h-4 fill-current" />
            Continue Learning
          </Link>
        </div>

        {/* ================================================================== */}
        {/* B. LEARNING ACTIVITY STATS                                          */}
        {/* ================================================================== */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-800 flex items-center gap-2">
              <Activity className="w-4 h-4 text-violet-600" />
              My Learning Activity
            </h2>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            <StatCard
              icon={BookOpen}
              label="Total Modules"
              value={summary?.total_topics_count ?? 0}
              color="violet"
            />
            <StatCard
              icon={CheckCircle2}
              label="Completed"
              value={summary?.completed_topics_count ?? 0}
              color="green"
            />
            <StatCard
              icon={Clock}
              label="In Progress"
              value={summary?.in_progress_topics_count ?? 0}
              color="orange"
            />
            <StatCard
              icon={Circle}
              label="Pending"
              value={summary?.pending_topics_count ?? 0}
              color="gray"
            />
            <StatCard
              icon={Award}
              label="Assessments Taken"
              value={summary?.total_assessment_attempts ?? 0}
              color="blue"
            />
          </div>
        </section>

        {/* ================================================================== */}
        {/* MAIN GRID: Progress + Activity + Phases + Quick Actions             */}
        {/* ================================================================== */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* LEFT COLUMN (col-span-2) */}
          <div className="lg:col-span-2 space-y-6">

            {/* ============================================================== */}
            {/* C. ROADMAP PROGRESS CARD                                        */}
            {/* ============================================================== */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                    <Map className="w-4 h-4 text-violet-600" />
                    My Roadmap Progress
                  </h2>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {summary?.career_title || 'AI Engineer'} Path
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-black text-violet-600">
                    {summary?.overall_progress ?? 0}%
                  </div>
                  <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
                    Overall
                  </div>
                </div>
              </div>

              {/* Info chips */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-center">
                  <div className="text-[10px] text-slate-500 font-semibold">Selected Career</div>
                  <div className="text-xs font-bold text-slate-800 mt-1 truncate">
                    {summary?.career_title || '—'}
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-center">
                  <div className="text-[10px] text-slate-500 font-semibold">Current Phase</div>
                  <div className="text-xs font-bold text-violet-700 mt-1">
                    {summary?.current_phase_name || 'Beginner'}
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-center">
                  <div className="text-[10px] text-slate-500 font-semibold">Phases Done</div>
                  <div className="text-xs font-bold text-green-600 mt-1">
                    {summary?.completed_phases_count ?? 0} / 3
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-center">
                  <div className="text-[10px] text-slate-500 font-semibold">Latest Score</div>
                  <div className={`text-xs font-bold mt-1 ${
                    summary?.latest_assessment_score >= 80 ? 'text-green-600' :
                    summary?.latest_assessment_score !== null && summary?.latest_assessment_score !== undefined
                      ? 'text-orange-500' : 'text-slate-400'
                  }`}>
                    {summary?.latest_assessment_score !== null && summary?.latest_assessment_score !== undefined
                      ? `${summary.latest_assessment_score}%`
                      : 'No attempt'}
                  </div>
                </div>
              </div>

              {/* Overall progress bar */}
              <div>
                <div className="flex justify-between text-xs font-semibold text-slate-500 mb-1.5">
                  <span>Roadmap Completion</span>
                  <span>
                    {summary?.completed_topics_count ?? 0} / {summary?.total_topics_count ?? 0} Topics
                  </span>
                </div>
                <div className="w-full h-3 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-violet-600 transition-all duration-700"
                    style={{ width: `${summary?.overall_progress ?? 0}%` }}
                  />
                </div>
              </div>

              {/* Next recommended action */}
              {summary?.next_recommended_action && (
                <div className="flex items-start gap-3 p-3.5 rounded-xl bg-violet-50 border border-violet-100">
                  <Sparkles className="w-4 h-4 text-violet-600 shrink-0 mt-0.5" />
                  <p className="text-xs font-semibold text-violet-900">
                    {summary.next_recommended_action}
                  </p>
                </div>
              )}
            </div>

            {/* ============================================================== */}
            {/* D. PHASE STATUS CARDS                                           */}
            {/* ============================================================== */}
            <div>
              <h2 className="text-base font-bold text-slate-800 mb-4 flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-violet-600" />
                Phase Status
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <PhaseCard phase={beginnerPhase}     index={0} />
                <PhaseCard phase={intermediatePhase} index={1} />
                <PhaseCard phase={advancedPhase}     index={2} />
              </div>
            </div>

          </div>

          {/* RIGHT COLUMN */}
          <div className="space-y-6">

            {/* ============================================================== */}
            {/* F. QUICK ACTIONS                                                */}
            {/* ============================================================== */}
            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
              <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
                <Zap className="w-4 h-4 text-violet-600" />
                Quick Actions
              </h3>

              <Link
                to="/roadmap"
                className="flex items-center justify-between p-3.5 rounded-xl border border-violet-200
                           bg-violet-600 hover:bg-violet-700 text-white transition-colors group"
              >
                <div className="flex items-center gap-2.5">
                  <Play className="w-4 h-4 fill-current" />
                  <span className="text-sm font-bold">Continue Learning</span>
                </div>
                <ChevronRight className="w-4 h-4 opacity-70 group-hover:translate-x-0.5 transition-transform" />
              </Link>

              <Link
                to="/roadmap"
                className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200
                           hover:border-violet-300 hover:bg-violet-50 transition-colors group"
              >
                <div className="flex items-center gap-2.5 text-slate-700">
                  <Map className="w-4 h-4 text-violet-500" />
                  <span className="text-sm font-semibold">View My Roadmap</span>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-violet-500 group-hover:translate-x-0.5 transition-all" />
              </Link>

              <Link
                to="/recommendations"
                className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200
                           hover:border-violet-300 hover:bg-violet-50 transition-colors group"
              >
                <div className="flex items-center gap-2.5 text-slate-700">
                  <Target className="w-4 h-4 text-violet-500" />
                  <span className="text-sm font-semibold">Career Recommendations</span>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-violet-500 group-hover:translate-x-0.5 transition-all" />
              </Link>

              {/* Take Assessment – enabled only when eligible */}
              {eligibleAssessmentPhase ? (
                <Link
                  to="/roadmap"
                  className="flex items-center justify-between p-3.5 rounded-xl border border-green-200
                             bg-green-50 hover:bg-green-100 transition-colors group"
                >
                  <div className="flex items-center gap-2.5 text-green-700">
                    <ClipboardCheck className="w-4 h-4" />
                    <div>
                      <div className="text-sm font-bold">Take Assessment</div>
                      <div className="text-[10px] text-green-600">
                        {eligibleAssessmentPhase.name} is ready!
                      </div>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-green-400 group-hover:translate-x-0.5 transition-transform" />
                </Link>
              ) : (
                <div className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200
                                bg-slate-50 opacity-60 cursor-not-allowed">
                  <div className="flex items-center gap-2.5 text-slate-400">
                    <ClipboardCheck className="w-4 h-4" />
                    <div>
                      <div className="text-sm font-semibold">Take Assessment</div>
                      <div className="text-[10px]">Complete all phase topics first</div>
                    </div>
                  </div>
                  <Lock className="w-4 h-4 text-slate-300" />
                </div>
              )}
            </div>

            {/* ============================================================== */}
            {/* E. RECENT ACTIVITY                                              */}
            {/* ============================================================== */}
            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-1">
              <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2 mb-3">
                <CheckSquare className="w-4 h-4 text-violet-600" />
                Recent Activity
              </h3>

              {activity.length === 0 ? (
                <div className="py-8 flex flex-col items-center text-center gap-2">
                  <BookOpen className="w-8 h-8 text-slate-300" />
                  <p className="text-xs text-slate-500 max-w-[180px] leading-relaxed">
                    No learning activity yet. Start your roadmap to see your progress here.
                  </p>
                  <Link
                    to="/roadmap"
                    className="mt-2 px-4 py-1.5 text-xs font-bold rounded-lg bg-violet-600 text-white hover:bg-violet-700 transition-colors"
                  >
                    Start Learning
                  </Link>
                </div>
              ) : (
                <div className="divide-y divide-slate-100">
                  {activity.map((a, idx) => (
                    <ActivityItem key={idx} activity={a} />
                  ))}
                  <div className="pt-3 text-center">
                    <Link
                      to="/roadmap"
                      className="text-xs font-semibold text-violet-600 hover:text-violet-700 flex items-center justify-center gap-1"
                    >
                      View all activity <ArrowRight className="w-3 h-3" />
                    </Link>
                  </div>
                </div>
              )}
            </div>

          </div>
        </div>

      </div>

      {/* Gemini Chatbot – preserved as-is */}
      <ChatbotWidget />
    </div>
  );
};

export default Dashboard;
