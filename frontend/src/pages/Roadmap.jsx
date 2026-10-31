import React, { useState, useEffect } from 'react';
import { roadmapService } from '../services/roadmapService';
import ChatbotWidget from '../components/ChatbotWidget';
import { 
  Map, 
  CheckCircle2, 
  Play, 
  Clock, 
  Sparkles, 
  BookOpen, 
  ClipboardCheck, 
  Code2, 
  Terminal, 
  UploadCloud, 
  Loader2, 
  RefreshCw,
  TrendingUp,
  Target,
  Lock,
  Unlock,
  AlertTriangle,
  XCircle,
  ChevronRight,
  RotateCcw,
  CheckSquare,
  Square,
  HelpCircle,
  Award,
  History,
  ArrowRight,
  Info,
  ExternalLink,
  ChevronDown,
  Layers,
  Check,
  Video,
  FileText,
  AlertCircle
} from 'lucide-react';

const Roadmap = () => {
  const [loading, setLoading] = useState(true);
  const [roadmap, setRoadmap] = useState(null);
  const [toastMessage, setToastMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Topic Learning Modal State
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [topicLoading, setTopicLoading] = useState(false);
  const [activeLearningTab, setActiveLearningTab] = useState('lesson'); // 'lesson', 'code', 'exercises', 'resources', 'check'
  const [practiceAnswer, setPracticeAnswer] = useState('');
  const [completingTopic, setCompletingTopic] = useState(false);

  // Phase Assessment Modal State
  const [assessmentPhase, setAssessmentPhase] = useState(null);
  const [assessmentData, setAssessmentData] = useState(null);
  const [assessmentAnswers, setAssessmentAnswers] = useState({});
  const [assessmentLoading, setAssessmentLoading] = useState(false);
  const [assessmentResult, setAssessmentResult] = useState(null);
  const [assessmentHistory, setAssessmentHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  const fetchRoadmap = async () => {
    setLoading(true);
    try {
      const data = await roadmapService.getRoadmap();
      setRoadmap(data);
    } catch (err) {
      console.error("Error fetching roadmap:", err);
      showError("Failed to load roadmap. Please verify your connection.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, []);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 5000);
  };

  const showError = (msg) => {
    setErrorMessage(msg);
    setTimeout(() => setErrorMessage(null), 6000);
  };

  // Open Learning Page for specific module
  const handleStartLearning = async (phaseId, topicId) => {
    setTopicLoading(true);
    setSelectedTopic(null);
    setActiveLearningTab('lesson');
    setPracticeAnswer('');

    try {
      const material = await roadmapService.getTopicMaterials(phaseId, topicId);
      setSelectedTopic(material);
    } catch (err) {
      const detail = err.response?.data?.detail || "Could not load topic learning materials.";
      showError(detail);
    } finally {
      setTopicLoading(false);
    }
  };

  // Complete Topic with verified signal
  const handleCompleteTopic = async () => {
    if (!selectedTopic) return;
    setCompletingTopic(true);

    try {
      const res = await roadmapService.completeTopic(
        selectedTopic.phase_id,
        selectedTopic.topic_id,
        practiceAnswer || null
      );
      setRoadmap(res.roadmap);
      setSelectedTopic(prev => ({ ...prev, completed: true, completed_at: res.completed_at }));
      showToast(`✓ Topic '${selectedTopic.module_title}' marked as COMPLETED! Progress updated.`);
    } catch (err) {
      const detail = err.response?.data?.detail || "Failed to complete topic. Check your answer or requirements.";
      showError(detail);
    } finally {
      setCompletingTopic(false);
    }
  };

  // Start Phase Assessment
  const handleOpenAssessment = async (phase) => {
    if (phase.status === 'LOCKED') {
      showError(`This phase is locked. ${phase.unlock_requirement}`);
      return;
    }
    if (!phase.all_topics_completed) {
      showError(`Complete all topics in ${phase.name} before attempting the assessment.`);
      return;
    }

    setAssessmentPhase(phase);
    setAssessmentLoading(true);
    setAssessmentResult(null);
    setAssessmentAnswers({});
    setShowHistory(false);

    try {
      const [quiz, history] = await Promise.all([
        roadmapService.generatePhaseAssessment(phase.phase_id),
        roadmapService.getPhaseAssessmentHistory(phase.phase_id)
      ]);
      setAssessmentData(quiz);
      setAssessmentHistory(history);
    } catch (err) {
      const detail = err.response?.data?.detail || "Could not generate assessment.";
      showError(detail);
      setAssessmentPhase(null);
    } finally {
      setAssessmentLoading(false);
    }
  };

  // Select Assessment Answer
  const handleSelectAnswer = (qId, optionVal) => {
    setAssessmentAnswers(prev => ({
      ...prev,
      [qId]: optionVal
    }));
  };

  // Submit Phase Assessment
  const handleSubmitAssessment = async () => {
    if (!assessmentPhase) return;
    setAssessmentLoading(true);

    try {
      const res = await roadmapService.submitPhaseAssessment(assessmentPhase.phase_id, assessmentAnswers);
      setAssessmentResult(res);
      setRoadmap(res.roadmap);

      // Refresh attempt history
      const history = await roadmapService.getPhaseAssessmentHistory(assessmentPhase.phase_id);
      setAssessmentHistory(history);

      if (res.passed) {
        showToast(`🎉 Congratulations! You passed with ${res.percentage}%! Next phase unlocked.`);
      } else {
        showError(`Score: ${res.percentage}%. You need at least 80% to pass. Review weak topics and retry.`);
      }
    } catch (err) {
      const detail = err.response?.data?.detail || "Error submitting assessment answers.";
      showError(detail);
    } finally {
      setAssessmentLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
        <Loader2 className="w-10 h-10 text-indigo-600 animate-spin" />
        <p className="text-sm font-medium text-slate-500">Loading your personalized career roadmap...</p>
      </div>
    );
  }

  const overallProgress = roadmap?.overall_progress || 0;
  const phases = roadmap?.phases || [];
  const completedTopics = roadmap?.completed_topics || [];
  const pendingTopics = roadmap?.pending_topics || [];
  const currentLearning = roadmap?.current_learning_topic;

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fade-in pb-20 relative">
      {/* Toast Notifications */}
      {toastMessage && (
        <div className="fixed top-6 right-6 z-50 p-4 rounded-xl bg-emerald-600 text-white shadow-xl flex items-center space-x-3 text-sm animate-in fade-in slide-in-from-top-2">
          <CheckCircle2 className="w-5 h-5 shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}
      {errorMessage && (
        <div className="fixed top-6 right-6 z-50 p-4 rounded-xl bg-red-600 text-white shadow-xl flex items-center space-x-3 text-sm animate-in fade-in slide-in-from-top-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 1. ROADMAP PROGRESS DASHBOARD (Section 8)                                */}
      {/* ========================================================================= */}
      <div className="rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 md:p-8 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-100 dark:border-slate-800">
          <div>
            <div className="flex items-center space-x-2 text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
              <Target className="w-4 h-4" />
              <span>Target Career Roadmap</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-black text-slate-900 dark:text-white mt-1 tracking-tight">
              {roadmap?.career_title || "AI Engineer"}
            </h1>
            <p className="text-slate-500 dark:text-slate-400 text-sm mt-1 max-w-2xl">
              {roadmap?.description}
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={fetchRoadmap}
              className="p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
              title="Refresh Roadmap"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
            <div className="text-right">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Overall Progress</span>
              <div className="text-3xl font-black text-indigo-600 dark:text-indigo-400">
                {overallProgress}%
              </div>
            </div>
          </div>
        </div>

        {/* Overall Progress Bar */}
        <div className="mt-6">
          <div className="flex justify-between text-xs font-semibold text-slate-600 dark:text-slate-400 mb-2">
            <span>Overall Roadmap Completion</span>
            <span>{completedTopics.length} of {roadmap?.total_topics_count || 15} Topics Completed</span>
          </div>
          <div className="w-full h-3 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-indigo-500 via-indigo-600 to-emerald-500 transition-all duration-700 ease-out"
              style={{ width: `${overallProgress}%` }}
            />
          </div>
        </div>

        {/* 3 Phase Cards Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          {phases.map((p, idx) => {
            const isCompleted = p.status === 'COMPLETED';
            const isLocked = p.status === 'LOCKED';
            const isActive = p.status === 'AVAILABLE' || p.status === 'IN_PROGRESS';

            return (
              <div 
                key={p.phase_id}
                className={`p-5 rounded-xl border transition-all ${
                  isCompleted 
                    ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-800/60'
                    : isActive
                    ? 'bg-blue-50/50 dark:bg-blue-950/20 border-blue-300 dark:border-blue-800/60 shadow-sm'
                    : 'bg-slate-50/60 dark:bg-slate-900/40 border-slate-200 dark:border-slate-800 opacity-80'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    Phase {idx + 1}
                  </span>
                  {isCompleted && (
                    <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300 flex items-center space-x-1">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>COMPLETED</span>
                    </span>
                  )}
                  {isActive && (
                    <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 flex items-center space-x-1">
                      <Unlock className="w-3 h-3" />
                      <span>UNLOCKED</span>
                    </span>
                  )}
                  {isLocked && (
                    <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 flex items-center space-x-1">
                      <Lock className="w-3 h-3" />
                      <span>LOCKED</span>
                    </span>
                  )}
                </div>

                <h3 className="text-base font-bold text-slate-900 dark:text-white mt-2">
                  {p.name}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 line-clamp-1">
                  {p.description}
                </p>

                <div className="mt-4 pt-3 border-t border-slate-200/60 dark:border-slate-800 flex items-center justify-between text-xs">
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase font-semibold">Topics Progress</span>
                    <span className="font-bold text-slate-800 dark:text-slate-200">
                      {p.completed_topics_count} / {p.total_topics_count} ({p.progress_percentage}%)
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-slate-400 block text-[10px] uppercase font-semibold">Best Assessment</span>
                    <span className={`font-bold ${
                      p.best_score >= 80 ? 'text-emerald-600 dark:text-emerald-400' :
                      p.best_score !== null ? 'text-amber-600 dark:text-amber-400' : 'text-slate-400'
                    }`}>
                      {p.best_score !== null ? `${p.best_score}% (Req: 80%)` : 'Not Taken'}
                    </span>
                  </div>
                </div>

                {isLocked && (
                  <div className="mt-3 text-[11px] text-slate-500 dark:text-slate-400 italic flex items-center space-x-1.5">
                    <Lock className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <span>Req: {p.unlock_requirement}</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Current Focus Banner */}
        <div className="mt-6 p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-lg bg-indigo-600 text-white shrink-0">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                Next Recommended Step
              </span>
              <p className="text-sm font-semibold text-slate-900 dark:text-white">
                {roadmap?.next_recommended_action}
              </p>
            </div>
          </div>
          {currentLearning && (
            <button
              onClick={() => handleStartLearning(currentLearning.phase_id, currentLearning.id)}
              className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-colors flex items-center space-x-2 shrink-0 self-start sm:self-auto shadow-sm"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Resume Learning</span>
            </button>
          )}
        </div>
      </div>

      {/* ========================================================================= */}
      {/* 2. THREE PROGRESSIVE PHASES (Sections 3, 4, 5, 6, 7)                     */}
      {/* ========================================================================= */}
      <div className="space-y-6">
        {phases.map((phase, pIdx) => {
          const isPhaseCompleted = phase.status === 'COMPLETED';
          const isPhaseLocked = phase.status === 'LOCKED';
          const isPhaseActive = !isPhaseCompleted && !isPhaseLocked;

          return (
            <div
              key={phase.phase_id}
              className={`rounded-2xl border transition-all overflow-hidden ${
                isPhaseCompleted
                  ? 'border-emerald-300 dark:border-emerald-800/80 bg-white dark:bg-slate-900 shadow-sm'
                  : isPhaseActive
                  ? 'border-indigo-300 dark:border-indigo-800/80 bg-white dark:bg-slate-900 shadow-md ring-1 ring-indigo-500/20'
                  : 'border-slate-200 dark:border-slate-800 bg-slate-50/40 dark:bg-slate-900/30 opacity-75'
              }`}
            >
              {/* Phase Header */}
              <div className={`p-6 border-b flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                isPhaseCompleted
                  ? 'bg-emerald-500/5 border-emerald-100 dark:border-emerald-900/40'
                  : isPhaseActive
                  ? 'bg-indigo-500/5 border-indigo-100 dark:border-indigo-900/40'
                  : 'bg-slate-100/50 dark:bg-slate-800/30 border-slate-200 dark:border-slate-800'
              }`}>
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-black uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                      Phase {phase.phase_number}
                    </span>
                    <span className="text-slate-300 dark:text-slate-700">•</span>
                    <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                      {phase.difficulty}
                    </span>
                    <span className="text-slate-300 dark:text-slate-700">•</span>
                    <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                      Passing Score: {phase.passing_score}%
                    </span>
                  </div>
                  <h2 className="text-xl font-black text-slate-900 dark:text-white flex items-center space-x-2.5">
                    <span>{phase.name}</span>
                    {isPhaseCompleted && (
                      <span className="p-1 rounded-full bg-emerald-500 text-white">
                        <Check className="w-3.5 h-3.5 stroke-[3]" />
                      </span>
                    )}
                    {isPhaseLocked && (
                      <span className="p-1 rounded-full bg-slate-400 text-white">
                        <Lock className="w-3.5 h-3.5" />
                      </span>
                    )}
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 max-w-2xl">
                    {phase.description}
                  </p>
                </div>

                <div className="flex items-center space-x-3 shrink-0">
                  {isPhaseCompleted && (
                    <span className="px-3 py-1.5 rounded-full text-xs font-bold bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700 flex items-center space-x-1.5">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>PHASE PASSED (80%+)</span>
                    </span>
                  )}
                  {isPhaseActive && (
                    <span className="px-3 py-1.5 rounded-full text-xs font-bold bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300 border border-indigo-300 dark:border-indigo-700 flex items-center space-x-1.5">
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>CURRENT PHASE</span>
                    </span>
                  )}
                  {isPhaseLocked && (
                    <span className="px-3 py-1.5 rounded-full text-xs font-bold bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-300 dark:border-slate-700 flex items-center space-x-1.5">
                      <Lock className="w-3.5 h-3.5" />
                      <span>LOCKED</span>
                    </span>
                  )}
                </div>
              </div>

              {/* Modules Grid */}
              <div className="p-6">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
                  Learning Modules & Topics ({phase.completed_topics_count} of {phase.total_topics_count} Completed)
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {phase.modules.map((mod) => {
                    const isModCompleted = mod.completed;
                    const canStart = !isPhaseLocked;

                    return (
                      <div
                        key={mod.id}
                        className={`p-4 rounded-xl border flex flex-col justify-between transition-all ${
                          isModCompleted
                            ? 'bg-emerald-50/40 dark:bg-emerald-950/10 border-emerald-300 dark:border-emerald-800/60 shadow-xs'
                            : canStart
                            ? 'bg-white dark:bg-slate-800/80 border-slate-200 dark:border-slate-700/80 hover:border-indigo-300 dark:hover:border-indigo-700 shadow-sm'
                            : 'bg-slate-100/50 dark:bg-slate-900/30 border-slate-200 dark:border-slate-800 opacity-60'
                        }`}
                      >
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 flex items-center space-x-1">
                              <Clock className="w-3 h-3" />
                              <span>{mod.estimated_duration}</span>
                            </span>

                            {isModCompleted ? (
                              <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center space-x-1">
                                <CheckCircle2 className="w-3.5 h-3.5" />
                                <span>Completed</span>
                              </span>
                            ) : canStart ? (
                              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400">
                                Incomplete
                              </span>
                            ) : (
                              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-200 dark:bg-slate-800 text-slate-500 flex items-center space-x-1">
                                <Lock className="w-3 h-3" />
                                <span>Locked</span>
                              </span>
                            )}
                          </div>

                          <h3 className="text-sm font-bold text-slate-900 dark:text-white leading-snug">
                            {mod.module_title}
                          </h3>

                          <ul className="text-[11px] text-slate-500 dark:text-slate-400 space-y-1">
                            {mod.learning_objectives?.slice(0, 2).map((obj, oIdx) => (
                              <li key={oIdx} className="flex items-start space-x-1.5">
                                <span className="text-indigo-500 font-bold">•</span>
                                <span className="line-clamp-1">{obj}</span>
                              </li>
                            ))}
                          </ul>
                        </div>

                        {/* Start Learning Button (Section 4) */}
                        <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                          <button
                            onClick={() => handleStartLearning(phase.phase_id, mod.id)}
                            disabled={!canStart}
                            className={`w-full py-2 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center space-x-1.5 ${
                              isModCompleted
                                ? 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 dark:hover:bg-emerald-900/60 border border-emerald-200 dark:border-emerald-800'
                                : canStart
                                ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-xs active:scale-98'
                                : 'bg-slate-200 dark:bg-slate-800 text-slate-400 cursor-not-allowed'
                            }`}
                          >
                            {isModCompleted ? (
                              <>
                                <Check className="w-3.5 h-3.5" />
                                <span>Review Topic</span>
                              </>
                            ) : canStart ? (
                              <>
                                <Play className="w-3.5 h-3.5 fill-current" />
                                <span>Start Learning</span>
                              </>
                            ) : (
                              <>
                                <Lock className="w-3.5 h-3.5" />
                                <span>Phase Locked</span>
                              </>
                            )}
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Phase Assessment Banner & Action (Section 7) */}
                <div className={`mt-6 p-5 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                  isPhaseCompleted
                    ? 'bg-emerald-500/10 border-emerald-300 dark:border-emerald-800'
                    : phase.all_topics_completed && !isPhaseLocked
                    ? 'bg-indigo-500/10 border-indigo-300 dark:border-indigo-800 ring-2 ring-indigo-500/20 animate-pulse'
                    : 'bg-slate-50 dark:bg-slate-800/40 border-slate-200 dark:border-slate-800'
                }`}>
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2">
                      <ClipboardCheck className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                      <span className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                        {phase.name} Assessment (80% Passing Rule)
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      {isPhaseCompleted
                        ? `You have passed this phase with a verified score of ${phase.best_score}%.`
                        : isPhaseLocked
                        ? `Phase assessment is locked. ${phase.unlock_requirement}.`
                        : phase.all_topics_completed
                        ? 'All topics completed! Take the phase assessment now. Score 80% or higher to unlock the next phase.'
                        : `Complete all ${phase.total_topics_count} topics in this phase to unlock this assessment.`}
                    </p>
                  </div>

                  <div className="flex items-center space-x-2 shrink-0">
                    <button
                      onClick={() => handleOpenAssessment(phase)}
                      disabled={isPhaseLocked || !phase.all_topics_completed}
                      className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center space-x-2 ${
                        isPhaseCompleted
                          ? 'bg-emerald-600 hover:bg-emerald-700 text-white'
                          : phase.all_topics_completed && !isPhaseLocked
                          ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-md active:scale-95'
                          : 'bg-slate-200 dark:bg-slate-800 text-slate-400 cursor-not-allowed'
                      }`}
                    >
                      <ClipboardCheck className="w-4 h-4" />
                      <span>
                        {isPhaseCompleted ? 'Retake Assessment' : 'Take Phase Assessment'}
                      </span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* ========================================================================= */}
      {/* 3. TOPIC LEARNING MODAL / VIEW (Sections 4, 5, 6)                        */}
      {/* ========================================================================= */}
      {selectedTopic && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-900/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full max-w-4xl max-h-[90vh] bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col overflow-hidden">
            {/* Modal Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40">
              <div className="space-y-1">
                <div className="flex items-center space-x-2 text-xs font-bold text-indigo-600 dark:text-indigo-400">
                  <span>{selectedTopic.phase_name}</span>
                  <span>•</span>
                  <span className="flex items-center space-x-1 text-slate-500">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{selectedTopic.estimated_duration}</span>
                  </span>
                  {selectedTopic.completed && (
                    <>
                      <span>•</span>
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 flex items-center space-x-1">
                        <CheckCircle2 className="w-3 h-3" />
                        <span>Completed</span>
                      </span>
                    </>
                  )}
                </div>
                <h2 className="text-xl font-black text-slate-900 dark:text-white">
                  {selectedTopic.module_title}
                </h2>
              </div>
              <button
                onClick={() => setSelectedTopic(null)}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                <XCircle className="w-6 h-6" />
              </button>
            </div>

            {/* Navigation Tabs */}
            <div className="flex items-center space-x-2 px-6 py-2.5 border-b border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-x-auto text-xs font-bold">
              <button
                onClick={() => setActiveLearningTab('lesson')}
                className={`px-3 py-1.5 rounded-lg transition-colors flex items-center space-x-1.5 ${
                  activeLearningTab === 'lesson'
                    ? 'bg-indigo-600 text-white'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Lesson & Explanation</span>
              </button>
              <button
                onClick={() => setActiveLearningTab('code')}
                className={`px-3 py-1.5 rounded-lg transition-colors flex items-center space-x-1.5 ${
                  activeLearningTab === 'code'
                    ? 'bg-indigo-600 text-white'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                <Code2 className="w-3.5 h-3.5" />
                <span>Code Examples</span>
              </button>
              <button
                onClick={() => setActiveLearningTab('exercises')}
                className={`px-3 py-1.5 rounded-lg transition-colors flex items-center space-x-1.5 ${
                  activeLearningTab === 'exercises'
                    ? 'bg-indigo-600 text-white'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                <Terminal className="w-3.5 h-3.5" />
                <span>Practical Exercise & Project</span>
              </button>
              <button
                onClick={() => setActiveLearningTab('resources')}
                className={`px-3 py-1.5 rounded-lg transition-colors flex items-center space-x-1.5 ${
                  activeLearningTab === 'resources'
                    ? 'bg-indigo-600 text-white'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Official Docs & Videos</span>
              </button>
              <button
                onClick={() => setActiveLearningTab('check')}
                className={`px-3 py-1.5 rounded-lg transition-colors flex items-center space-x-1.5 ${
                  activeLearningTab === 'check'
                    ? 'bg-indigo-600 text-white'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                <CheckSquare className="w-3.5 h-3.5" />
                <span>Knowledge Check & Complete</span>
              </button>
            </div>

            {/* Modal Content Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 text-sm">
              {/* Learning Objectives Callout */}
              <div className="p-4 rounded-xl bg-indigo-50/60 dark:bg-indigo-950/20 border border-indigo-200/60 dark:border-indigo-800/40">
                <h4 className="text-xs font-bold text-indigo-700 dark:text-indigo-400 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                  <Target className="w-4 h-4" />
                  <span>Topic Learning Objectives</span>
                </h4>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-700 dark:text-slate-300">
                  {selectedTopic.learning_objectives?.map((obj, i) => (
                    <li key={i} className="flex items-start space-x-2">
                      <Check className="w-3.5 h-3.5 text-indigo-500 shrink-0 mt-0.5" />
                      <span>{obj}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* TAB 1: Lesson & Explanation */}
              {activeLearningTab === 'lesson' && (
                <div className="space-y-6">
                  <div className="prose dark:prose-invert max-w-none text-slate-700 dark:text-slate-300 leading-relaxed text-sm">
                    <p className="font-medium text-base text-slate-900 dark:text-white">
                      {selectedTopic.lesson}
                    </p>
                  </div>

                  {selectedTopic.step_by_step_explanation && (
                    <div className="space-y-3">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Step-by-Step Concepts Breakdown
                      </h4>
                      <div className="space-y-2.5">
                        {selectedTopic.step_by_step_explanation.map((step, idx) => (
                          <div key={idx} className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300">
                            {step}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: Code Examples */}
              {activeLearningTab === 'code' && (
                <div className="space-y-6">
                  {selectedTopic.code_examples?.map((ex, idx) => (
                    <div key={idx} className="rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden">
                      <div className="px-4 py-2.5 bg-slate-100 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-800 dark:text-slate-200 flex items-center space-x-2">
                          <Code2 className="w-4 h-4 text-indigo-500" />
                          <span>{ex.title}</span>
                        </span>
                      </div>
                      <div className="p-4 bg-slate-900 text-emerald-400 font-mono text-xs overflow-x-auto">
                        <pre className="whitespace-pre-wrap">{ex.code}</pre>
                      </div>
                      <div className="p-3.5 bg-slate-50 dark:bg-slate-850 text-xs text-slate-600 dark:text-slate-400 border-t border-slate-200 dark:border-slate-800">
                        <strong>Explanation:</strong> {ex.explanation}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* TAB 3: Practical Exercise & Project */}
              {activeLearningTab === 'exercises' && (
                <div className="space-y-6">
                  {selectedTopic.practical_exercises?.map((pe, idx) => (
                    <div key={idx} className="p-4 rounded-xl border border-slate-200 dark:border-slate-700/80 bg-slate-50/50 dark:bg-slate-800/40 space-y-2">
                      <h4 className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider flex items-center space-x-2">
                        <Terminal className="w-4 h-4" />
                        <span>{pe.title}</span>
                      </h4>
                      <p className="text-xs text-slate-700 dark:text-slate-300">
                        {pe.instructions}
                      </p>
                    </div>
                  ))}

                  {selectedTopic.mini_project && (
                    <div className="p-5 rounded-xl border border-indigo-200 dark:border-indigo-800/60 bg-indigo-50/20 dark:bg-indigo-950/20 space-y-3">
                      <h4 className="text-sm font-bold text-indigo-700 dark:text-indigo-400 flex items-center space-x-2">
                        <Sparkles className="w-4 h-4" />
                        <span>{selectedTopic.mini_project.title}</span>
                      </h4>
                      <div className="space-y-2">
                        <span className="text-xs font-semibold text-slate-600 dark:text-slate-300">Implementation Steps:</span>
                        <ul className="space-y-1.5 text-xs text-slate-600 dark:text-slate-400">
                          {selectedTopic.mini_project.steps?.map((st, i) => (
                            <li key={i} className="flex items-start space-x-2">
                              <span className="font-bold text-indigo-500">{i + 1}.</span>
                              <span>{st}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div className="pt-2 text-xs text-slate-500 dark:text-slate-400 italic">
                        <strong>Expected Outcome:</strong> {selectedTopic.mini_project.expected_outcome}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 4: Resources & Videos */}
              {activeLearningTab === 'resources' && (
                <div className="space-y-6">
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-1.5">
                      <FileText className="w-4 h-4 text-indigo-500" />
                      <span>Official Documentation</span>
                    </h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {selectedTopic.documentation?.map((doc, idx) => (
                        <a
                          key={idx}
                          href={doc.url}
                          target="_blank"
                          rel="noreferrer"
                          className="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-indigo-500 dark:hover:border-indigo-500 transition-colors flex items-center justify-between group"
                        >
                          <span className="text-xs font-bold text-slate-800 dark:text-slate-200 group-hover:text-indigo-600 dark:group-hover:text-indigo-400">
                            {doc.title}
                          </span>
                          <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-indigo-500" />
                        </a>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-1.5">
                      <Video className="w-4 h-4 text-emerald-500" />
                      <span>Curated Educational Videos</span>
                    </h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {selectedTopic.curated_videos?.map((vid, idx) => (
                        <a
                          key={idx}
                          href={vid.url}
                          target="_blank"
                          rel="noreferrer"
                          className="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-emerald-500 dark:hover:border-emerald-500 transition-colors flex items-center justify-between group"
                        >
                          <span className="text-xs font-bold text-slate-800 dark:text-slate-200 group-hover:text-emerald-600 dark:group-hover:text-emerald-400">
                            {vid.title}
                          </span>
                          <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-emerald-500" />
                        </a>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 5: Knowledge Check & Complete */}
              {activeLearningTab === 'check' && (
                <div className="space-y-6">
                  <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-850 space-y-4">
                    <div className="flex items-center space-x-2 text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                      <CheckSquare className="w-4 h-4" />
                      <span>Mandatory Topic Knowledge Check</span>
                    </div>

                    <p className="text-sm font-semibold text-slate-900 dark:text-white">
                      {selectedTopic.knowledge_check?.question}
                    </p>

                    <div className="space-y-2">
                      {selectedTopic.knowledge_check?.options?.map((opt, i) => (
                        <label
                          key={i}
                          onClick={() => setPracticeAnswer(opt)}
                          className={`flex items-center space-x-3 p-3 rounded-xl border text-xs cursor-pointer transition-all ${
                            practiceAnswer === opt
                              ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-900 dark:text-indigo-200 font-bold'
                              : 'border-slate-200 dark:border-slate-700 hover:bg-white dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
                          }`}
                        >
                          <input
                            type="radio"
                            name="practiceOption"
                            checked={practiceAnswer === opt}
                            onChange={() => setPracticeAnswer(opt)}
                            className="text-indigo-600 focus:ring-indigo-500"
                          />
                          <span>{opt}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/60 flex items-center justify-between">
                    <div>
                      <h4 className="text-xs font-bold text-emerald-800 dark:text-emerald-300">
                        {selectedTopic.completed ? 'Topic Verified & Completed ✓' : 'Finish Learning Requirements'}
                      </h4>
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                        {selectedTopic.completed
                          ? `Completed on ${new Date(selectedTopic.completed_at).toLocaleDateString()}. This topic counts towards your phase progress.`
                          : 'Select the correct knowledge check answer above to complete this topic and unlock progress.'}
                      </p>
                    </div>

                    <button
                      onClick={handleCompleteTopic}
                      disabled={completingTopic || !practiceAnswer || selectedTopic.completed}
                      className={`px-5 py-2.5 rounded-xl text-xs font-bold transition-all shadow-md active:scale-95 flex items-center space-x-2 ${
                        selectedTopic.completed
                          ? 'bg-emerald-500 text-white cursor-not-allowed opacity-90'
                          : 'bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white'
                      }`}
                    >
                      {completingTopic ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Check className="w-4 h-4 stroke-[3]" />
                      )}
                      <span>{selectedTopic.completed ? 'Completed ✓' : 'Mark Topic as Completed'}</span>
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-3 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40 flex items-center justify-between text-xs">
              <span className="text-slate-400">
                Study sequence: Read Lesson → Inspect Code → Solve Exercises → Verify Knowledge Check
              </span>
              <button
                onClick={() => setSelectedTopic(null)}
                className="px-4 py-2 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold hover:bg-slate-300 dark:hover:bg-slate-700 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 4. PHASE ASSESSMENT MODAL (80% Passing Rule) (Section 7)                 */}
      {/* ========================================================================= */}
      {assessmentPhase && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-900/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full max-w-3xl max-h-[90vh] bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white">
              <div>
                <span className="text-xs font-bold text-indigo-200 uppercase tracking-wider">
                  Phase Assessment • {assessmentPhase.difficulty}
                </span>
                <h3 className="text-lg font-black text-white">
                  {assessmentPhase.name} Assessment
                </h3>
              </div>
              <button
                onClick={() => setAssessmentPhase(null)}
                className="p-1.5 rounded-lg text-indigo-200 hover:text-white hover:bg-white/10"
              >
                <XCircle className="w-6 h-6" />
              </button>
            </div>

            {/* Assessment Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 text-sm">
              {assessmentLoading && (
                <div className="py-12 flex flex-col items-center justify-center space-y-3 text-slate-500">
                  <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
                  <span className="text-xs font-semibold">Generating randomized assessment questions...</span>
                </div>
              )}

              {/* Assessment Results View */}
              {!assessmentLoading && assessmentResult && (
                <div className="space-y-6 animate-in fade-in">
                  <div className={`p-6 rounded-2xl border text-center space-y-3 ${
                    assessmentResult.passed
                      ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-800'
                      : 'bg-red-50 dark:bg-red-950/20 border-red-300 dark:border-red-800'
                  }`}>
                    <div className="flex justify-center">
                      {assessmentResult.passed ? (
                        <div className="p-3 rounded-full bg-emerald-500 text-white">
                          <CheckCircle2 className="w-10 h-10" />
                        </div>
                      ) : (
                        <div className="p-3 rounded-full bg-red-500 text-white">
                          <AlertTriangle className="w-10 h-10" />
                        </div>
                      )}
                    </div>

                    <h4 className="text-2xl font-black text-slate-900 dark:text-white">
                      Score: {assessmentResult.percentage}% ({assessmentResult.score} of {assessmentResult.total_questions} Correct)
                    </h4>

                    <div className="flex justify-center space-x-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-extrabold uppercase tracking-wider ${
                        assessmentResult.passed
                          ? 'bg-emerald-200 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200'
                          : 'bg-red-200 dark:bg-red-900 text-red-800 dark:text-red-200'
                      }`}>
                        {assessmentResult.passed ? 'PASSED (>= 80%)' : 'FAILED (< 80%)'}
                      </span>
                    </div>

                    <p className="text-xs text-slate-600 dark:text-slate-400 max-w-lg mx-auto">
                      {assessmentResult.message}
                    </p>
                  </div>

                  {/* Weak Topics to Revise */}
                  {assessmentResult.weak_topics?.length > 0 && (
                    <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/60 space-y-2">
                      <h4 className="text-xs font-bold text-amber-800 dark:text-amber-300 uppercase tracking-wider flex items-center space-x-1.5">
                        <AlertTriangle className="w-4 h-4" />
                        <span>Recommended Topics for Revision</span>
                      </h4>
                      <ul className="text-xs text-slate-700 dark:text-slate-300 space-y-1">
                        {assessmentResult.weak_topics.map((wt, i) => (
                          <li key={i} className="flex items-center space-x-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                            <span>{wt}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Itemized Review */}
                  <div className="space-y-4">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Answer Review & Explanations
                    </h4>
                    {assessmentResult.reviews?.map((rev, rIdx) => (
                      <div
                        key={rIdx}
                        className={`p-4 rounded-xl border text-xs space-y-2 ${
                          rev.is_correct
                            ? 'bg-emerald-50/40 dark:bg-emerald-950/10 border-emerald-200 dark:border-emerald-800/40'
                            : 'bg-red-50/40 dark:bg-red-950/10 border-red-200 dark:border-red-800/40'
                        }`}
                      >
                        <div className="flex items-center justify-between font-bold">
                          <span className="text-slate-800 dark:text-slate-200">
                            Q{rIdx + 1}: {rev.question}
                          </span>
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            rev.is_correct ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white'
                          }`}>
                            {rev.is_correct ? 'Correct' : 'Incorrect'}
                          </span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                          <div>
                            <span className="text-slate-400">Your Answer: </span>
                            <span className="font-semibold text-slate-800 dark:text-slate-200">{rev.user_answer}</span>
                          </div>
                          <div>
                            <span className="text-slate-400">Correct Answer: </span>
                            <span className="font-semibold text-emerald-600 dark:text-emerald-400">{rev.correct_answer}</span>
                          </div>
                        </div>
                        <div className="text-[11px] text-slate-500 dark:text-slate-400 pt-1 border-t border-slate-200/60 dark:border-slate-800">
                          <strong>Explanation:</strong> {rev.explanation}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Assessment Questions View */}
              {!assessmentLoading && !assessmentResult && assessmentData && (
                <div className="space-y-6">
                  <div className="p-3.5 rounded-xl bg-indigo-50/70 dark:bg-indigo-950/30 border border-indigo-200 dark:border-indigo-800 text-xs text-indigo-900 dark:text-indigo-200 flex items-center justify-between">
                    <span>
                      Pass Requirement: <strong>80% or higher ({Math.ceil(assessmentData.total_questions * 0.8)} of {assessmentData.total_questions} correct)</strong>
                    </span>
                    <span className="font-bold">
                      Answered: {Object.keys(assessmentAnswers).length} / {assessmentData.total_questions}
                    </span>
                  </div>

                  {assessmentData.questions?.map((q, idx) => (
                    <div
                      key={q.question_id}
                      className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/30 dark:bg-slate-850 space-y-3"
                    >
                      <div className="flex items-center justify-between text-xs font-bold text-slate-400">
                        <span>Question {idx + 1} of {assessmentData.total_questions}</span>
                        <span className="text-indigo-500">{q.topic}</span>
                      </div>
                      <p className="text-sm font-semibold text-slate-900 dark:text-white">
                        {q.question}
                      </p>

                      <div className="space-y-2">
                        {q.options?.map((opt, oIdx) => (
                          <label
                            key={oIdx}
                            onClick={() => handleSelectAnswer(q.question_id, opt)}
                            className={`flex items-center space-x-3 p-3 rounded-xl border text-xs cursor-pointer transition-all ${
                              assessmentAnswers[q.question_id] === opt
                                ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-900 dark:text-indigo-200 font-bold'
                                : 'border-slate-200 dark:border-slate-700 hover:bg-white dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
                            }`}
                          >
                            <input
                              type="radio"
                              name={`q_${q.question_id}`}
                              checked={assessmentAnswers[q.question_id] === opt}
                              onChange={() => handleSelectAnswer(q.question_id, opt)}
                              className="text-indigo-600 focus:ring-indigo-500"
                            />
                            <span>{opt}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-4 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40 flex items-center justify-between">
              <button
                onClick={() => setAssessmentPhase(null)}
                className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
              >
                Close
              </button>

              {!assessmentResult && assessmentData && (
                <button
                  onClick={handleSubmitAssessment}
                  disabled={assessmentLoading || Object.keys(assessmentAnswers).length < (assessmentData.total_questions || 10)}
                  className="px-6 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 text-white text-xs font-bold transition-all shadow-md active:scale-95 flex items-center space-x-2"
                >
                  {assessmentLoading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Check className="w-4 h-4 stroke-[3]" />
                  )}
                  <span>Submit Assessment for Grading</span>
                </button>
              )}

              {assessmentResult && !assessmentResult.passed && (
                <button
                  onClick={() => handleOpenAssessment(assessmentPhase)}
                  className="px-6 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-all shadow-md active:scale-95 flex items-center space-x-2"
                >
                  <RotateCcw className="w-4 h-4" />
                  <span>Retry Phase Assessment</span>
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 5. FLOATING GEMINI CHATBOT (ROADMAP PAGE ONLY - Section 9)               */}
      {/* ========================================================================= */}
      <ChatbotWidget />
    </div>
  );
};

export default Roadmap;
