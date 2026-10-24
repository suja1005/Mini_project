import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { profileService } from '../services/profileService';
import { assessmentService } from '../services/assessmentService';
import { recommendationService } from '../services/recommendationService';
import { evidenceService } from '../services/evidenceService';
import { roadmapService } from '../services/roadmapService';
import { progressService } from '../services/progressService';
import MetricCard from '../components/MetricCard';
import PhaseBanner from '../components/PhaseBanner';
import { 
  UserCheck, 
  Award, 
  Compass, 
  TrendingUp, 
  ArrowRight,
  ShieldCheck, 
  Map, 
  BarChart3,
  Loader2, 
  AlertCircle,
  CheckCircle2,
  Sparkles,
  Paperclip,
  Mic,
  Lightbulb,
  Send,
  Plus,
  FileText,
  Layers,
  ArrowUpRight,
  Bot,
  X,
  Target
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [assessment, setAssessment] = useState(null);
  const [topCareer, setTopCareer] = useState(null);
  const [evidence, setEvidence] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [progress, setProgress] = useState(null);

  // AI Chat & Prompt Bar state
  const [promptText, setPromptText] = useState('');
  const [showPromptSuggestions, setShowPromptSuggestions] = useState(false);
  const [isVoiceActive, setIsVoiceActive] = useState(false);
  const [aiResponse, setAiResponse] = useState(null);
  const [aiGenerating, setAiGenerating] = useState(false);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        const [profData, passRes, recData, evData, rmData, progData] = await Promise.allSettled([
          profileService.getProfile(),
          assessmentService.getResults(),
          recommendationService.getRecommendations(),
          evidenceService.getEvidence(),
          roadmapService.getRoadmap(),
          progressService.getProgress()
        ]);

        if (profData.status === 'fulfilled') setProfile(profData.value);
        if (passRes.status === 'fulfilled') setAssessment(passRes.value);
        if (recData.status === 'fulfilled' && recData.value?.top_recommendations?.length > 0) {
          setTopCareer(recData.value.top_recommendations[0]);
        }
        if (evData.status === 'fulfilled') setEvidence(evData.value);
        if (rmData.status === 'fulfilled') setRoadmap(rmData.value);
        if (progData.status === 'fulfilled') setProgress(progData.value);
      } catch (err) {
        console.error("Error fetching dashboard data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const isProfileComplete = profile?.is_complete ?? false;
  const isAssessmentComplete = assessment?.is_completed ?? false;

  const currentEmp = progress?.current_employability || roadmap?.current_employability || 58;
  const targetEmp = progress?.target_employability || roadmap?.target_employability || 80;
  const empGap = progress?.employability_gap || roadmap?.employability_gap || Math.max(0, targetEmp - currentEmp);
  const avgConfidence = evidence?.average_confidence || 65;
  const completedTasks = roadmap?.completed_tasks || 0;
  const totalTasks = roadmap?.total_tasks || 1;
  const progressPct = roadmap?.progress_percentage || 0;

  // Next recommended task from roadmap
  const nextTask = roadmap?.tasks?.find(t => t.status !== 'COMPLETED') || roadmap?.tasks?.[0];

  // Quick prompt suggestions
  const suggestedPrompts = [
    "Summarize my employability gap for AI Engineer role",
    "Which verified skills should I target next to reach 80%?",
    "How does the Evidence Engine recalculate my confidence score?",
    "Generate an accelerated 4-week milestones schedule"
  ];

  const handleSendPrompt = (textToSend) => {
    const query = textToSend || promptText;
    if (!query.trim()) return;

    setAiGenerating(true);
    setAiResponse(null);

    // Simulate smart contextual AI response based on student data
    setTimeout(() => {
      let responseBody = {
        title: "AI Career Guidance Analysis",
        query: query,
        summary: `Based on your verified skills and current profile for ${topCareer ? topCareer.title : 'AI Engineer'}:`,
        points: [
          `Your current employability score is ${currentEmp}%, with a target of ${targetEmp}% (Gap: ${empGap}%).`,
          `Evidence Engine has verified ${evidence?.total_verified || 0} skills with an average confidence of ${avgConfidence}%.`,
          `To close your gap fastest: complete the high-priority task "${nextTask?.title || 'Advanced Deep Learning Quiz'}" in your adaptive roadmap.`,
          `Submitting a verified GitHub repository or project artifact will boost your evidence confidence by up to +12%.`
        ],
        actionLabel: "Continue Roadmap Task",
        actionLink: "/roadmap"
      };

      setAiResponse(responseBody);
      setAiGenerating(false);
      setPromptText('');
      setShowPromptSuggestions(false);
    }, 600);
  };

  const handleVoiceToggle = () => {
    setIsVoiceActive(!isVoiceActive);
    if (!isVoiceActive) {
      setPromptText("How do I improve my career fit score for AI Engineer?");
    }
  };

  if (loading) {
    return (
      <div className="h-96 flex flex-col items-center justify-center space-y-3 text-slate-500">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
        <span className="text-sm font-medium">Loading AI Guidance Dashboard...</span>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-12 animate-fade-in">
      {/* Top Banner Notice */}
      <PhaseBanner 
        title="Phase 2 Integrated Platform Active"
        message="Evidence-Based Employability Enhancement Engine is online. Verified skills dynamically govern career readiness, adaptive roadmaps, and progress tracking."
      />

      {/* Hero Container - Clean SaaS layout matching the reference image */}
      <div className="bg-white dark:bg-[#111827] rounded-3xl border border-gray-200/80 dark:border-slate-800 p-6 md:p-10 shadow-xs space-y-8 transition-colors">
        {/* Welcome Headline */}
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h1 className="text-3xl md:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Welcome to CareerAI
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm md:text-base leading-relaxed">
            Get started by selecting a task and AI Career Advisor can guide the rest. Not sure where to start?
          </p>
        </div>

        {/* 2x2 Quick Action Cards (Exact layout from the reference image) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-3xl mx-auto">
          {/* Card 1: Skill Assessment (Soft Amber) */}
          <Link
            to="/assessment"
            className="group flex items-center justify-between p-4 rounded-2xl border border-gray-200/80 dark:border-slate-800 hover:border-amber-300 dark:hover:border-amber-600/50 bg-white dark:bg-[#162035] shadow-xs hover:shadow-md transition-all duration-200"
          >
            <div className="flex items-center space-x-3.5">
              <div className="w-11 h-11 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 border border-amber-200/60 dark:border-amber-800/40 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <FileText className="w-5 h-5" />
              </div>
              <div className="text-left">
                <div className="font-bold text-slate-900 dark:text-white text-sm">
                  Take Skill Assessment
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  Verify technical & logical baseline
                </div>
              </div>
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 group-hover:bg-amber-500 group-hover:text-white flex items-center justify-center transition-colors shrink-0">
              <Plus className="w-4 h-4" />
            </div>
          </Link>

          {/* Card 2: Explore Careers (Soft Cyan / Sky) */}
          <Link
            to="/recommendations"
            className="group flex items-center justify-between p-4 rounded-2xl border border-gray-200/80 dark:border-slate-800 hover:border-sky-300 dark:hover:border-sky-600/50 bg-white dark:bg-[#162035] shadow-xs hover:shadow-md transition-all duration-200"
          >
            <div className="flex items-center space-x-3.5">
              <div className="w-11 h-11 rounded-xl bg-sky-50 dark:bg-sky-950/40 text-sky-600 dark:text-sky-400 border border-sky-200/60 dark:border-sky-800/40 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <Compass className="w-5 h-5" />
              </div>
              <div className="text-left">
                <div className="font-bold text-slate-900 dark:text-white text-sm">
                  Explore Top Careers
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  Target AI & software roles with high fit
                </div>
              </div>
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 group-hover:bg-sky-500 group-hover:text-white flex items-center justify-center transition-colors shrink-0">
              <Plus className="w-4 h-4" />
            </div>
          </Link>

          {/* Card 3: Verify Evidence (Soft Emerald) */}
          <Link
            to="/evidence"
            className="group flex items-center justify-between p-4 rounded-2xl border border-gray-200/80 dark:border-slate-800 hover:border-emerald-300 dark:hover:border-emerald-600/50 bg-white dark:bg-[#162035] shadow-xs hover:shadow-md transition-all duration-200"
          >
            <div className="flex items-center space-x-3.5">
              <div className="w-11 h-11 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 border border-emerald-200/60 dark:border-emerald-800/40 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div className="text-left">
                <div className="font-bold text-slate-900 dark:text-white text-sm">
                  Verify Skill Evidence
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  Upload GitHub, certificates & projects
                </div>
              </div>
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 group-hover:bg-emerald-500 group-hover:text-white flex items-center justify-center transition-colors shrink-0">
              <Plus className="w-4 h-4" />
            </div>
          </Link>

          {/* Card 4: Milestone Roadmap (Soft Purple / Pink) */}
          <Link
            to="/roadmap"
            className="group flex items-center justify-between p-4 rounded-2xl border border-gray-200/80 dark:border-slate-800 hover:border-purple-300 dark:hover:border-purple-600/50 bg-white dark:bg-[#162035] shadow-xs hover:shadow-md transition-all duration-200"
          >
            <div className="flex items-center space-x-3.5">
              <div className="w-11 h-11 rounded-xl bg-purple-50 dark:bg-purple-950/40 text-purple-600 dark:text-purple-400 border border-purple-200/60 dark:border-purple-800/40 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <Map className="w-5 h-5" />
              </div>
              <div className="text-left">
                <div className="font-bold text-slate-900 dark:text-white text-sm">
                  Adaptive Roadmap
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  Take knowledge quizzes & verified tasks
                </div>
              </div>
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 group-hover:bg-purple-500 group-hover:text-white flex items-center justify-center transition-colors shrink-0">
              <Plus className="w-4 h-4" />
            </div>
          </Link>
        </div>

        {/* AI Guidance Prompt Bar (Matching bottom docked box in reference image) */}
        <div className="max-w-3xl mx-auto space-y-3">
          <div className="rounded-2xl border border-gray-300 dark:border-slate-700 bg-white dark:bg-[#0f172a] shadow-md p-3 space-y-2 focus-within:ring-2 focus-within:ring-indigo-500/30 focus-within:border-indigo-500 transition-all">
            <textarea
              rows={2}
              value={promptText}
              onChange={(e) => setPromptText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendPrompt();
                }
              }}
              placeholder="Ask AI Career Advisor anything (e.g. 'Summarize my readiness for AI Engineer', 'How to reach 80% employability?')..."
              className="w-full resize-none border-none bg-transparent text-sm text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-0 leading-relaxed"
            />

            <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-gray-100 dark:border-slate-800 text-xs">
              {/* Left action chips inside prompt */}
              <div className="flex items-center space-x-2">
                <Link
                  to="/evidence"
                  className="inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors font-medium"
                >
                  <Paperclip className="w-3.5 h-3.5" />
                  <span>Attach Evidence</span>
                </Link>

                <button
                  type="button"
                  onClick={handleVoiceToggle}
                  className={`inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-lg font-medium transition-colors ${
                    isVoiceActive 
                      ? 'bg-rose-50 text-rose-600 dark:bg-rose-950/40 dark:text-rose-400' 
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  <Mic className={`w-3.5 h-3.5 ${isVoiceActive ? 'animate-pulse text-rose-500' : ''}`} />
                  <span>{isVoiceActive ? 'Listening...' : 'Voice Guidance'}</span>
                </button>

                <button
                  type="button"
                  onClick={() => setShowPromptSuggestions(!showPromptSuggestions)}
                  className="inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors font-medium"
                >
                  <Lightbulb className="w-3.5 h-3.5 text-amber-500" />
                  <span>Browse Prompts</span>
                </button>
              </div>

              {/* Right: Character count & Send circular gradient button */}
              <div className="flex items-center space-x-3">
                <span className="text-[11px] text-slate-400">
                  {promptText.length} / 3,000
                </span>
                <button
                  type="button"
                  onClick={() => handleSendPrompt()}
                  disabled={aiGenerating || !promptText.trim()}
                  className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white flex items-center justify-center shadow-md shadow-indigo-500/25 disabled:opacity-40 transition-all active:scale-95"
                >
                  {aiGenerating ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Send className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Browse Prompt Suggestions Popover */}
          {showPromptSuggestions && (
            <div className="p-3 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200 dark:border-slate-800 space-y-2 animate-fade-in">
              <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider px-1">
                Suggested Career Guidance Prompts
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {suggestedPrompts.map((p, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSendPrompt(p)}
                    className="text-left text-xs p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-gray-200/60 dark:border-slate-700 hover:border-indigo-300 text-slate-700 dark:text-slate-300 hover:text-indigo-600 transition-all shadow-xs"
                  >
                    "{p}"
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* AI Response Card */}
          {aiResponse && (
            <div className="p-5 rounded-2xl bg-indigo-50/70 dark:bg-[#18233c] border border-indigo-200/80 dark:border-indigo-500/30 space-y-3 animate-fade-in">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-indigo-700 dark:text-indigo-400 font-bold text-sm">
                  <Bot className="w-4 h-4" />
                  <span>{aiResponse.title}</span>
                </div>
                <button
                  type="button"
                  onClick={() => setAiResponse(null)}
                  className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-white"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>

              <div className="text-xs text-slate-600 dark:text-slate-300 italic">
                Query: "{aiResponse.query}"
              </div>

              <ul className="text-xs space-y-2 text-slate-700 dark:text-slate-200 bg-white/80 dark:bg-slate-900/60 p-3.5 rounded-xl border border-indigo-100 dark:border-slate-800">
                {aiResponse.points.map((pt, i) => (
                  <li key={i} className="flex items-start space-x-2">
                    <span className="text-indigo-500 font-bold">•</span>
                    <span>{pt}</span>
                  </li>
                ))}
              </ul>

              <div className="flex justify-end pt-1">
                <Link
                  to={aiResponse.actionLink}
                  className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-sm transition-all"
                >
                  <span>{aiResponse.actionLabel}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          )}

          <div className="text-center text-[11px] text-slate-400">
            Script may generate inaccurate information about people, places, or facts. Model: CareerAI Guidance v2.0
          </div>
        </div>
      </div>

      {/* Profile & Assessment Warning Alerts if incomplete */}
      {(!isProfileComplete || !isAssessmentComplete) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {!isProfileComplete && (
            <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/40 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <AlertCircle className="w-5 h-5 text-amber-500 shrink-0" />
                <div className="text-xs text-slate-700 dark:text-amber-200">
                  <span className="font-bold block text-sm text-slate-900 dark:text-amber-100">Profile Incomplete</span>
                  Complete your AI profile to unlock personalized recommendations.
                </div>
              </div>
              <Link to="/profile" className="px-3.5 py-1.5 bg-amber-500 hover:bg-amber-400 text-white font-bold rounded-xl text-xs shrink-0 shadow-xs">
                Complete Profile
              </Link>
            </div>
          )}

          {!isAssessmentComplete && (
            <div className="p-4 rounded-2xl bg-indigo-50 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-800/40 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <AlertCircle className="w-5 h-5 text-indigo-500 shrink-0" />
                <div className="text-xs text-slate-700 dark:text-indigo-200">
                  <span className="font-bold block text-sm text-slate-900 dark:text-indigo-100">Assessment Pending</span>
                  Take the skill assessment to verify logical & technical score.
                </div>
              </div>
              <Link to="/assessment" className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl text-xs shrink-0 shadow-xs">
                Take Assessment
              </Link>
            </div>
          )}
        </div>
      )}

      {/* Phase 2 Enhanced Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <MetricCard 
          title="Current Readiness"
          value={`${currentEmp}%`}
          subtitle={`Target: ${targetEmp}%`}
          icon={TrendingUp}
          color="emerald"
          badge="Live"
        />
        <MetricCard 
          title="Employability Gap"
          value={`${empGap}%`}
          subtitle="Points to Target"
          icon={UserCheck}
          color="amber"
        />
        <MetricCard 
          title="Evidence Confidence"
          value={`${avgConfidence}%`}
          subtitle={evidence?.overall_evidence_status || "Partially Verified"}
          icon={ShieldCheck}
          color="cyan"
        />
        <MetricCard 
          title="Roadmap Progress"
          value={`${progressPct}%`}
          subtitle={`${completedTasks} of ${totalTasks} Tasks`}
          icon={Map}
          color="indigo"
        />
        <MetricCard 
          title="Verified Skills"
          value={`${evidence?.total_verified || 0}`}
          subtitle="Proven Competencies"
          icon={CheckCircle2}
          color="purple"
        />
      </div>

      {/* Main Grid: Left Detailed Status & Right Career Track Cards (matching right side panel in image) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Top Match & Active Roadmap Priority */}
        <div className="lg:col-span-2 space-y-6">
          {/* Career Fit & Achievability Summary Card */}
          <div className="bg-white dark:bg-[#111827] p-6 rounded-3xl border border-gray-200/80 dark:border-slate-800 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-slate-900 dark:text-white">
                  Career Fit & Achievability Summary
                </h2>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Dynamically computed based on dual-verified evidence
                </p>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
                Verified Model
              </span>
            </div>

            <div className="p-5 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200/60 dark:border-slate-700/60 space-y-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-800 dark:text-slate-200 font-semibold">
                  Top Recommended: {topCareer ? topCareer.title : "AI Engineer"}
                </span>
                <span className="text-indigo-600 dark:text-indigo-400 font-extrabold text-base">
                  {topCareer ? topCareer.fit_score : 87}% Fit
                </span>
              </div>
              
              <div className="w-full bg-gray-200 dark:bg-slate-700 h-2.5 rounded-full overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-full rounded-full transition-all duration-500"
                  style={{ width: `${topCareer ? topCareer.fit_score : 87}%` }}
                />
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-center">
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800/80 border border-gray-200/70 dark:border-slate-700/80">
                  <div className="text-[11px] text-slate-500 dark:text-slate-400">Current Readiness</div>
                  <div className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">{currentEmp}%</div>
                </div>
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800/80 border border-gray-200/70 dark:border-slate-700/80">
                  <div className="text-[11px] text-slate-500 dark:text-slate-400">Employability Gap</div>
                  <div className="text-sm font-bold text-amber-600 dark:text-amber-400 mt-0.5">{empGap}%</div>
                </div>
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800/80 border border-gray-200/70 dark:border-slate-700/80">
                  <div className="text-[11px] text-slate-500 dark:text-slate-400">Verified Skills</div>
                  <div className="text-sm font-bold text-indigo-600 dark:text-indigo-300 mt-0.5">{evidence?.total_verified || 0} Proven</div>
                </div>
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800/80 border border-gray-200/70 dark:border-slate-700/80">
                  <div className="text-[11px] text-slate-500 dark:text-slate-400">Roadmap Tasks</div>
                  <div className="text-sm font-bold text-cyan-600 dark:text-cyan-400 mt-0.5">{completedTasks}/{totalTasks} Done</div>
                </div>
              </div>

              <div className="pt-2 flex justify-between items-center text-xs">
                <Link 
                  to="/evidence"
                  className="text-slate-600 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-white flex items-center space-x-1.5 font-semibold"
                >
                  <ShieldCheck className="w-4 h-4 text-indigo-500" />
                  <span>Review Evidence Breakdown</span>
                </Link>

                <Link 
                  to={`/career/${topCareer ? topCareer.id : 'ai-engineer'}`}
                  className="font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center space-x-1"
                >
                  <span>Decision & Risk Details</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </div>

          {/* Active Next Task Card */}
          {nextTask && (
            <div className="bg-white dark:bg-[#111827] p-6 rounded-3xl border border-indigo-200 dark:border-indigo-500/30 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Sparkles className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  <h3 className="text-base font-bold text-slate-900 dark:text-white">Next Priority Roadmap Action</h3>
                </div>
                <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold border ${
                  nextTask.priority === 'HIGH' 
                    ? 'bg-red-50 text-red-600 border-red-200 dark:bg-red-950/40 dark:text-red-400 dark:border-red-800' 
                    : 'bg-amber-50 text-amber-600 border-amber-200 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800'
                }`}>
                  {nextTask.priority} Priority
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200/60 dark:border-slate-700/60 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-300">{nextTask.type} • {nextTask.skill}</span>
                  <span className="text-[11px] text-slate-500">Effort: {nextTask.estimated_effort}</span>
                </div>
                <h4 className="text-base font-bold text-slate-900 dark:text-white">{nextTask.title}</h4>
                <p className="text-xs text-slate-600 dark:text-slate-400 line-clamp-2">{nextTask.description}</p>
              </div>

              <div className="flex justify-end">
                <Link
                  to="/roadmap"
                  className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center space-x-2 shadow-xs transition-all active:scale-95"
                >
                  <span>Continue Roadmap</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Projects / Career Goals Panel (matching the right-side list in the image!) */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-[#111827] p-6 rounded-3xl border border-gray-200/80 dark:border-slate-800 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                Career Goals (3)
              </h2>
              <Link 
                to="/recommendations"
                className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center space-x-1"
              >
                <span>View All</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
            </div>

            {/* List of Tracks */}
            <div className="space-y-2.5">
              {/* Item 1: Primary Target */}
              <Link
                to="/career/ai-engineer"
                className="block p-3.5 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200/70 dark:border-slate-700 hover:border-indigo-300 transition-all group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                    AI Engineer
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-400">
                    Active
                  </span>
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 flex items-center justify-between">
                  <span>Match: 87% • Verified</span>
                  <span className="text-indigo-600 dark:text-indigo-400 font-semibold">{currentEmp}% / {targetEmp}%</span>
                </div>
              </Link>

              {/* Item 2 */}
              <Link
                to="/career/full-stack-developer"
                className="block p-3.5 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200/70 dark:border-slate-700 hover:border-indigo-300 transition-all group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                    Full Stack Developer
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-300">
                    Alternative
                  </span>
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 flex items-center justify-between">
                  <span>Match: 82% • High Demand</span>
                  <span className="text-slate-500 font-semibold">3 Tasks left</span>
                </div>
              </Link>

              {/* Item 3 */}
              <Link
                to="/career/data-scientist"
                className="block p-3.5 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200/70 dark:border-slate-700 hover:border-indigo-300 transition-all group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                    Data Scientist
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-300">
                    Recommended
                  </span>
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 flex items-center justify-between">
                  <span>Match: 76% • Math & ML</span>
                  <span className="text-slate-500 font-semibold">Explore</span>
                </div>
              </Link>
            </div>

            {/* Quick Action Button */}
            <Link
              to="/recommendations"
              className="w-full py-2.5 rounded-xl border border-dashed border-gray-300 dark:border-slate-700 hover:border-indigo-500 text-slate-600 dark:text-slate-400 hover:text-indigo-600 flex items-center justify-center space-x-1.5 text-xs font-semibold transition-all"
            >
              <Plus className="w-4 h-4" />
              <span>Explore New Career Trajectory</span>
            </Link>
          </div>

          {/* Quick Access to Phase 2 Modules */}
          <div className="bg-white dark:bg-[#111827] p-6 rounded-3xl border border-gray-200/80 dark:border-slate-800 shadow-xs space-y-3">
            <h3 className="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
              Quick Shortcuts
            </h3>
            <div className="grid grid-cols-1 gap-2">
              <Link 
                to="/evidence" 
                className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 hover:bg-indigo-50 dark:hover:bg-indigo-950/30 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:text-indigo-600 transition-colors"
              >
                <div className="flex items-center space-x-2.5">
                  <ShieldCheck className="w-4 h-4 text-indigo-500" />
                  <span>Upload Evidence & Projects</span>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
              </Link>
              <Link 
                to="/progress" 
                className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 hover:bg-indigo-50 dark:hover:bg-indigo-950/30 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:text-indigo-600 transition-colors"
              >
                <div className="flex items-center space-x-2.5">
                  <BarChart3 className="w-4 h-4 text-cyan-500" />
                  <span>Progress Trend Charts</span>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
