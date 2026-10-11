import React, { useState, useEffect } from 'react';
import { roadmapService } from '../services/roadmapService';
import PhaseBanner from '../components/PhaseBanner';
import MetricCard from '../components/MetricCard';
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
  Info
} from 'lucide-react';

const Roadmap = () => {
  const [loading, setLoading] = useState(true);
  const [updatingTaskId, setUpdatingTaskId] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [filterType, setFilterType] = useState('ALL');
  const [toastMessage, setToastMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Modal / Drawer state
  const [selectedTask, setSelectedTask] = useState(null);
  const [isQuizActive, setIsQuizActive] = useState(false);
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [userAnswers, setUserAnswers] = useState({});
  const [quizLoading, setQuizLoading] = useState(false);
  const [quizResult, setQuizResult] = useState(null);
  const [attemptHistory, setAttemptHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('learning'); // 'learning', 'quiz', 'history'

  const fetchRoadmap = async () => {
    setLoading(true);
    try {
      const data = await roadmapService.getRoadmap();
      setRoadmap(data);

      // If selectedTask is open, refresh its data
      if (selectedTask) {
        const freshTask = data.tasks.find(t => t.id === selectedTask.id);
        if (freshTask) setSelectedTask(freshTask);
      }
    } catch (err) {
      console.error("Error fetching roadmap:", err);
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
    setTimeout(() => setErrorMessage(null), 5000);
  };

  // Open Task Detail
  const handleOpenTask = async (task) => {
    setSelectedTask(task);
    setIsQuizActive(false);
    setQuizResult(null);
    setUserAnswers({});
    setActiveTab('learning');

    // Fetch attempt history
    try {
      const history = await roadmapService.getVerificationHistory(task.id);
      setAttemptHistory(history);
    } catch (err) {
      console.error("Error loading verification history:", err);
    }
  };

  const handleCloseTask = () => {
    setSelectedTask(null);
    setIsQuizActive(false);
    setQuizResult(null);
    setUserAnswers({});
  };

  // Start Task
  const handleStartTask = async (taskId) => {
    setUpdatingTaskId(taskId);
    try {
      const updated = await roadmapService.startTask(taskId);
      setRoadmap(updated);
      const updatedTask = updated.tasks.find(t => t.id === taskId);
      if (updatedTask) setSelectedTask(updatedTask);
      showToast("Task started! Study the topics and complete the subtopics checklist.");
    } catch (err) {
      showError(err.response?.data?.detail || "Could not start task.");
    } finally {
      setUpdatingTaskId(null);
    }
  };

  // Toggle Subtopic Checkbox
  const handleToggleSubtopic = async (topicId, subtopicId, currentVal) => {
    if (!selectedTask) return;
    if (selectedTask.status === 'LOCKED') return;

    try {
      const updated = await roadmapService.toggleSubtopic(
        selectedTask.id,
        topicId,
        subtopicId,
        !currentVal
      );
      setRoadmap(updated);
      const freshTask = updated.tasks.find(t => t.id === selectedTask.id);
      if (freshTask) setSelectedTask(freshTask);
    } catch (err) {
      showError("Failed to update topic status.");
    }
  };

  // Complete Learning Button
  const handleCompleteLearning = async (taskId) => {
    setUpdatingTaskId(taskId);
    try {
      const updated = await roadmapService.completeLearning(taskId);
      setRoadmap(updated);
      const freshTask = updated.tasks.find(t => t.id === taskId);
      if (freshTask) setSelectedTask(freshTask);
      showToast("Learning completed! Click 'Generate Questions' to verify your knowledge.");
    } catch (err) {
      showError(err.response?.data?.detail || "Please complete all subtopics before verifying.");
    } finally {
      setUpdatingTaskId(null);
    }
  };

  // Generate Quiz Questions
  const handleGenerateQuestions = async (taskId) => {
    setQuizLoading(true);
    setUserAnswers({});
    setQuizResult(null);
    try {
      const questions = await roadmapService.generateQuestions(taskId);
      setQuizQuestions(questions);
      setIsQuizActive(true);
      setActiveTab('quiz');
      showToast(`Generated ${questions.length} new verification questions matching task topics.`);
    } catch (err) {
      showError(err.response?.data?.detail || "Failed to generate questions.");
    } finally {
      setQuizLoading(false);
    }
  };

  // Option Select
  const handleOptionSelect = (questionId, optionValue) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionId]: optionValue
    }));
  };

  // Submit Quiz Verification
  const handleSubmitQuiz = async () => {
    if (!selectedTask) return;
    setQuizLoading(true);
    try {
      const result = await roadmapService.submitVerification(selectedTask.id, userAnswers);
      setQuizResult(result);
      setIsQuizActive(false);

      // Refresh roadmap
      const updatedRoadmap = await roadmapService.getRoadmap();
      setRoadmap(updatedRoadmap);

      const freshTask = updatedRoadmap.tasks.find(t => t.id === selectedTask.id);
      if (freshTask) setSelectedTask(freshTask);

      // Refresh history
      const history = await roadmapService.getVerificationHistory(selectedTask.id);
      setAttemptHistory(history);

      if (result.passed) {
        showToast("🎉 Learning Verified Successfully! Next task unlocked.");
      } else {
        showError(`Verification score is ${result.percentage}% (Required: 70%). Review weak topics and try again.`);
      }
    } catch (err) {
      showError(err.response?.data?.detail || "Error submitting quiz.");
    } finally {
      setQuizLoading(false);
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'Learning': return <BookOpen className="w-4 h-4 text-indigo-400" />;
      case 'Assessment': return <ClipboardCheck className="w-4 h-4 text-emerald-400" />;
      case 'Project': return <Code2 className="w-4 h-4 text-amber-400" />;
      case 'Practice': return <Terminal className="w-4 h-4 text-cyan-400" />;
      case 'Evidence Submission': return <UploadCloud className="w-4 h-4 text-purple-400" />;
      default: return <BookOpen className="w-4 h-4 text-indigo-400" />;
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'VERIFIED':
        return (
          <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center space-x-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>VERIFIED ✓</span>
          </span>
        );
      case 'LEARNING_COMPLETED':
        return (
          <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 flex items-center space-x-1">
            <Award className="w-3.5 h-3.5 text-cyan-400" />
            <span>LEARNING COMPLETED</span>
          </span>
        );
      case 'IN_PROGRESS':
        return (
          <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 flex items-center space-x-1 animate-pulse">
            <Clock className="w-3.5 h-3.5 text-indigo-400" />
            <span>IN PROGRESS</span>
          </span>
        );
      case 'FAILED':
        return (
          <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-red-500/20 text-red-300 border border-red-500/40 flex items-center space-x-1">
            <XCircle className="w-3.5 h-3.5 text-red-400" />
            <span>VERIFICATION FAILED</span>
          </span>
        );
      case 'LOCKED':
        return (
          <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-slate-800 text-slate-400 border border-slate-700 flex items-center space-x-1">
            <Lock className="w-3.5 h-3.5 text-slate-500" />
            <span>LOCKED 🔒</span>
          </span>
        );
      default:
        return (
          <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700 flex items-center space-x-1">
            <Unlock className="w-3.5 h-3.5 text-slate-400" />
            <span>NOT STARTED</span>
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Loading Adaptive Verification Roadmap...</span>
      </div>
    );
  }

  const tasks = roadmap?.tasks || [];
  const filteredTasks = tasks.filter(t => {
    if (filterType === 'ALL') return true;
    if (filterType === 'HIGH') return t.priority === 'HIGH';
    if (filterType === 'VERIFIED') return t.status === 'VERIFIED';
    if (filterType === 'IN_PROGRESS') return t.status === 'IN_PROGRESS';
    if (filterType === 'LOCKED') return t.status === 'LOCKED';
    return t.type.toLowerCase().includes(filterType.toLowerCase());
  });

  const groupedPhases = [1, 2, 3, 4, 5].map(phaseNum => {
    const phaseTasks = filteredTasks.filter(t => t.phase === phaseNum);
    const phaseName = roadmap?.phases?.[phaseNum - 1] || `Phase ${phaseNum}`;
    return { phaseNum, phaseName, tasks: phaseTasks };
  }).filter(g => g.tasks.length > 0);

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center space-x-3">
            <Map className="w-8 h-8 text-indigo-400" />
            <span>Learning & Verification Roadmap</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Target Role: <span className="text-white font-bold">{roadmap?.career_title}</span> — Learn topics, complete subtopics, and verify understanding via dynamic quizzes.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={fetchRoadmap}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold flex items-center space-x-2 transition-all"
          >
            <RefreshCw className="w-4 h-4 text-indigo-400" />
            <span>Refresh Progress</span>
          </button>
        </div>
      </div>

      <PhaseBanner 
        title="Knowledge Verification Workflow"
        message="Roadmap progress requires real proof of learning: Study Topics → Toggle Subtopics → Mark Learning Complete → Pass Dynamic 5-Question Quiz (>= 70%) → Unlock Next Task."
      />

      {toastMessage && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center space-x-2 shadow-lg shadow-emerald-500/10 animate-fadeIn">
          <Sparkles className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {errorMessage && (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs font-semibold flex items-center space-x-2 shadow-lg shadow-red-500/10 animate-fadeIn">
          <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <MetricCard 
          title="Verified Roadmap Progress" 
          value={`${roadmap?.progress_percentage}%`} 
          subtitle={`${roadmap?.verified_tasks} of ${roadmap?.total_tasks} Tasks Verified`} 
          icon={Award} 
          color="emerald" 
        />
        <MetricCard 
          title="Current Employability" 
          value={`${roadmap?.current_employability}%`} 
          subtitle="Skill-Verified Model" 
          icon={TrendingUp} 
          color="indigo" 
        />
        <MetricCard 
          title="Target Employability" 
          value={`${roadmap?.target_employability}%`} 
          subtitle={`Required for ${roadmap?.career_title}`} 
          icon={Target} 
          color="cyan" 
        />
        <MetricCard 
          title="Employability Gap" 
          value={`${roadmap?.employability_gap}%`} 
          subtitle="Points to Target" 
          icon={TrendingUp} 
          color="amber" 
        />
      </div>

      {/* Progress Bar */}
      <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-2">
        <div className="flex justify-between text-xs font-semibold">
          <span className="text-slate-300">Overall Verified Roadmap Completion</span>
          <span className="text-indigo-400">{roadmap?.verified_tasks} / {roadmap?.total_tasks} Verified Tasks ({roadmap?.progress_percentage}%)</span>
        </div>
        <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
          <div 
            className="bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-400 h-full rounded-full transition-all duration-500"
            style={{ width: `${roadmap?.progress_percentage}%` }}
          ></div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 pt-1 border-b border-slate-800 pb-3">
        {[
          { key: 'ALL', label: 'All Tasks' },
          { key: 'HIGH', label: 'High Priority' },
          { key: 'IN_PROGRESS', label: 'In Progress ⏳' },
          { key: 'VERIFIED', label: 'Verified ✓' },
          { key: 'LOCKED', label: 'Locked 🔒' }
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setFilterType(tab.key)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
              filterType === tab.key
                ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/20'
                : 'bg-slate-900/80 text-slate-400 border-slate-800 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Phased Task Lists */}
      <div className="space-y-6">
        {groupedPhases.length === 0 ? (
          <div className="p-8 text-center text-slate-500 bg-slate-900/40 rounded-2xl border border-slate-800">
            No tasks match the selected filter.
          </div>
        ) : (
          groupedPhases.map(group => (
            <div key={group.phaseNum} className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-7 h-7 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 font-bold text-xs">
                  {group.phaseNum}
                </div>
                <h2 className="text-base font-bold text-white tracking-wide">
                  {group.phaseName}
                </h2>
                <span className="text-xs text-slate-500 font-medium">({group.tasks.length} tasks)</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {group.tasks.map(task => {
                  const isVerified = task.status === 'VERIFIED';
                  const isLocked = task.status === 'LOCKED';
                  const isInProgress = task.status === 'IN_PROGRESS';
                  const isLearningCompleted = task.status === 'LEARNING_COMPLETED';
                  const isFailed = task.status === 'FAILED';

                  return (
                    <div 
                      key={task.id} 
                      onClick={() => handleOpenTask(task)}
                      className={`p-5 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between space-y-4 hover:scale-[1.01] ${
                        isVerified 
                          ? 'bg-slate-900/40 border-emerald-500/30 shadow-lg shadow-emerald-500/5'
                          : isLearningCompleted
                          ? 'bg-slate-900/90 border-cyan-500/50 shadow-lg shadow-cyan-500/10'
                          : isInProgress
                          ? 'bg-slate-900/90 border-indigo-500/50 shadow-lg shadow-indigo-500/10'
                          : isFailed
                          ? 'bg-slate-900/80 border-red-500/40'
                          : isLocked
                          ? 'bg-slate-950/80 border-slate-800/60 opacity-60'
                          : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                      }`}
                    >
                      <div className="space-y-3">
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex items-center space-x-2">
                            <span className="p-1.5 rounded-lg bg-slate-800 border border-slate-700">
                              {getTypeIcon(task.type)}
                            </span>
                            <span className="text-[11px] font-semibold text-slate-400">
                              {task.type}
                            </span>
                          </div>

                          <div className="flex items-center space-x-2">
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                              task.difficulty === 'Beginner'
                                ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
                                : task.difficulty === 'Intermediate'
                                ? 'bg-amber-500/15 text-amber-400 border-amber-500/30'
                                : 'bg-purple-500/15 text-purple-400 border-purple-500/30'
                            }`}>
                              {task.difficulty}
                            </span>
                            {getStatusBadge(task.status)}
                          </div>
                        </div>

                        <div>
                          <h3 className={`text-base font-bold flex items-center justify-between ${isVerified ? 'text-slate-200' : 'text-white'}`}>
                            <span>{task.title}</span>
                            <ChevronRight className="w-4 h-4 text-slate-500" />
                          </h3>
                          <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                            {task.description}
                          </p>
                        </div>

                        {/* Learning Topics Summary preview */}
                        {task.topics && task.topics.length > 0 && (
                          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1.5">
                            <div className="flex justify-between text-[11px] font-semibold text-slate-400">
                              <span>Topics to Learn ({task.topics.length})</span>
                              <span className="text-indigo-400">{task.learning_progress_percentage}% studied</span>
                            </div>
                            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                              <div 
                                className="bg-indigo-500 h-full rounded-full transition-all duration-300"
                                style={{ width: `${task.learning_progress_percentage}%` }}
                              ></div>
                            </div>
                          </div>
                        )}

                        <div className="flex items-center space-x-4 text-xs text-slate-400 pt-1">
                          <span className="flex items-center space-x-1">
                            <Clock className="w-3.5 h-3.5 text-slate-500" />
                            <span>{task.estimated_hours}</span>
                          </span>
                          <span className="font-semibold text-indigo-400">
                            Skill: {task.skill}
                          </span>
                        </div>
                      </div>

                      {/* Card Footer */}
                      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                        {isLocked ? (
                          <span className="text-[11px] text-slate-500 flex items-center space-x-1 font-medium">
                            <Lock className="w-3 h-3 text-slate-500" />
                            <span>Complete previous task first</span>
                          </span>
                        ) : isVerified ? (
                          <span className="text-xs text-emerald-400 font-bold flex items-center space-x-1">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span>Verified (Quiz Score: {task.quiz_score ?? 'Pass'})</span>
                          </span>
                        ) : (
                          <span className="text-[11px] text-indigo-400 font-semibold flex items-center space-x-1">
                            <span>Click to view topics & verify</span>
                            <ArrowRight className="w-3 h-3" />
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))
        )}
      </div>

      {/* ========================================================================= */}
      {/* TASK DETAIL DRAWER / MODAL */}
      {/* ========================================================================= */}
      {selectedTask && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto animate-fadeIn">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl flex flex-col justify-between">
            {/* Modal Header */}
            <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4 sticky top-0 bg-slate-900/95 backdrop-blur z-10">
              <div>
                <div className="flex items-center space-x-2 mb-2">
                  <span className="px-2.5 py-0.5 rounded text-[11px] font-bold bg-slate-800 text-indigo-400 border border-slate-700">
                    Phase {selectedTask.phase}
                  </span>
                  <span className="px-2.5 py-0.5 rounded text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                    Difficulty: {selectedTask.difficulty}
                  </span>
                  <span className="px-2.5 py-0.5 rounded text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                    Estimated Time: {selectedTask.estimated_hours}
                  </span>
                  {getStatusBadge(selectedTask.status)}
                </div>
                <h2 className="text-xl md:text-2xl font-extrabold text-white">
                  {selectedTask.title}
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  {selectedTask.description}
                </p>
              </div>
              <button 
                onClick={handleCloseTask}
                className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-all shrink-0"
              >
                ✕
              </button>
            </div>

            {/* Modal Content Tabs */}
            <div className="p-6 space-y-6">
              {/* Tab Navigation */}
              <div className="flex border-b border-slate-800 space-x-4">
                <button
                  onClick={() => { setActiveTab('learning'); setIsQuizActive(false); }}
                  className={`pb-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-2 ${
                    activeTab === 'learning'
                      ? 'border-indigo-500 text-indigo-400'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <BookOpen className="w-4 h-4" />
                  <span>1. What You Need to Learn</span>
                </button>

                <button
                  onClick={() => setActiveTab('quiz')}
                  disabled={selectedTask.status === 'LOCKED'}
                  className={`pb-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-2 ${
                    activeTab === 'quiz'
                      ? 'border-indigo-500 text-indigo-400'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <HelpCircle className="w-4 h-4" />
                  <span>2. Verify Knowledge (Quiz)</span>
                </button>

                <button
                  onClick={() => setActiveTab('history')}
                  className={`pb-3 text-xs font-bold transition-all border-b-2 flex items-center space-x-2 ${
                    activeTab === 'history'
                      ? 'border-indigo-500 text-indigo-400'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <History className="w-4 h-4" />
                  <span>Attempt History ({attemptHistory.length})</span>
                </button>
              </div>

              {/* TAB 1: WHAT YOU NEED TO LEARN & SUBTOPICS */}
              {activeTab === 'learning' && (
                <div className="space-y-6">
                  {/* Task Lock Warning */}
                  {selectedTask.status === 'LOCKED' && (
                    <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold flex items-center space-x-3">
                      <Lock className="w-5 h-5 text-amber-400 shrink-0" />
                      <span>This task is locked. Complete and verify the previous prerequisite task first to unlock learning.</span>
                    </div>
                  )}

                  {/* Learning Progress Bar */}
                  <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-2">
                    <div className="flex justify-between text-xs font-semibold">
                      <span className="text-slate-300">Overall Learning Topics Progress</span>
                      <span className="text-indigo-400">{selectedTask.learning_progress_percentage}% Studied</span>
                    </div>
                    <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                      <div 
                        className="bg-indigo-500 h-full rounded-full transition-all duration-300"
                        style={{ width: `${selectedTask.learning_progress_percentage}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Learning Objectives */}
                  {selectedTask.learning_objectives && selectedTask.learning_objectives.length > 0 && (
                    <div className="space-y-2">
                      <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 flex items-center space-x-2">
                        <Target className="w-4 h-4 text-indigo-400" />
                        <span>Learning Objectives</span>
                      </h3>
                      <ul className="grid grid-cols-1 gap-2 bg-slate-950/60 p-4 rounded-2xl border border-slate-800/80">
                        {selectedTask.learning_objectives.map((obj, idx) => (
                          <li key={idx} className="text-xs text-slate-300 flex items-start space-x-2">
                            <span className="text-indigo-400 font-bold">•</span>
                            <span>{obj}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Topics and Subtopics Checklist */}
                  <div className="space-y-4">
                    <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 flex items-center space-x-2">
                      <CheckSquare className="w-4 h-4 text-emerald-400" />
                      <span>Topics & Subtopics Checklist</span>
                    </h3>

                    {selectedTask.topics.map((topic) => (
                      <div key={topic.id} className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                            <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
                            <span>{topic.title}</span>
                          </h4>
                          {topic.completed && (
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                              Topic Completed ✓
                            </span>
                          )}
                        </div>

                        {topic.description && (
                          <p className="text-xs text-slate-400">{topic.description}</p>
                        )}

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                          {topic.subtopics && topic.subtopics.map((sub) => (
                            <div 
                              key={sub.id}
                              onClick={() => handleToggleSubtopic(topic.id, sub.id, sub.completed)}
                              className={`p-3 rounded-xl border flex items-center justify-between cursor-pointer transition-all ${
                                sub.completed 
                                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-200' 
                                  : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700'
                              }`}
                            >
                              <span className="text-xs font-medium">{sub.title}</span>
                              {sub.completed ? (
                                <CheckSquare className="w-4 h-4 text-emerald-400 shrink-0" />
                              ) : (
                                <Square className="w-4 h-4 text-slate-600 shrink-0" />
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Task Status Actions */}
                  <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                    <div>
                      {selectedTask.status === 'NOT_STARTED' && (
                        <button
                          onClick={() => handleStartTask(selectedTask.id)}
                          disabled={updatingTaskId === selectedTask.id}
                          className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center space-x-2 shadow-lg shadow-indigo-600/20 transition-all disabled:opacity-50"
                        >
                          {updatingTaskId === selectedTask.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                          <span>Start Learning</span>
                        </button>
                      )}

                      {selectedTask.status === 'IN_PROGRESS' && (
                        <button
                          onClick={() => handleCompleteLearning(selectedTask.id)}
                          disabled={updatingTaskId === selectedTask.id}
                          className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center space-x-2 shadow-lg shadow-emerald-600/20 transition-all disabled:opacity-50"
                        >
                          {updatingTaskId === selectedTask.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                          <span>Mark Learning Complete</span>
                        </button>
                      )}

                      {(selectedTask.status === 'LEARNING_COMPLETED' || selectedTask.status === 'FAILED' || selectedTask.status === 'VERIFIED') && (
                        <button
                          onClick={() => handleGenerateQuestions(selectedTask.id)}
                          disabled={quizLoading}
                          className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center space-x-2 shadow-lg shadow-indigo-600/20 transition-all disabled:opacity-50"
                        >
                          {quizLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <HelpCircle className="w-4 h-4" />}
                          <span>{selectedTask.status === 'FAILED' ? 'Generate New Questions (Retry)' : 'Generate Verification Questions'}</span>
                        </button>
                      )}
                    </div>

                    <div className="text-right text-xs text-slate-400">
                      <span>Verification Rule: <strong className="text-white">&ge; 70% Score Required</strong></span>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 2: VERIFICATION QUIZ & RESULTS */}
              {activeTab === 'quiz' && (
                <div className="space-y-6">
                  {!isQuizActive && !quizResult && (
                    <div className="p-8 text-center space-y-4 bg-slate-950/60 rounded-3xl border border-slate-800">
                      <HelpCircle className="w-12 h-12 text-indigo-400 mx-auto" />
                      <h3 className="text-lg font-bold text-white">Knowledge Verification Assessment</h3>
                      <p className="text-xs text-slate-400 max-w-md mx-auto">
                        To verify your task completion, you must pass a dynamic 5-question test generated strictly from this task's topics.
                      </p>
                      <button
                        onClick={() => handleGenerateQuestions(selectedTask.id)}
                        disabled={quizLoading}
                        className="px-6 py-3 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center space-x-2 mx-auto shadow-lg shadow-indigo-600/20 transition-all disabled:opacity-50"
                      >
                        {quizLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                        <span>Generate 5 New Questions</span>
                      </button>
                    </div>
                  )}

                  {/* ACTIVE QUIZ SCREEN */}
                  {isQuizActive && quizQuestions.length > 0 && (
                    <div className="space-y-6">
                      <div className="flex justify-between items-center bg-slate-950/60 p-4 rounded-2xl border border-slate-800">
                        <div>
                          <span className="text-xs text-indigo-400 font-bold">Verification Test</span>
                          <h4 className="text-sm font-bold text-white">Answer all 5 questions</h4>
                        </div>
                        <span className="text-xs font-bold text-slate-400 bg-slate-800 px-3 py-1 rounded-xl">
                          Attempt #{selectedTask.attempts_count + 1}
                        </span>
                      </div>

                      <div className="space-y-6">
                        {quizQuestions.map((q, idx) => (
                          <div key={q.question_id} className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3">
                            <div className="flex items-center justify-between">
                              <span className="text-xs font-bold text-indigo-400">
                                Question {idx + 1} of {quizQuestions.length}
                              </span>
                              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                                Topic: {q.topic}
                              </span>
                            </div>

                            <p className="text-sm font-semibold text-white leading-relaxed">
                              {q.question}
                            </p>

                            <div className="grid grid-cols-1 gap-2 pt-2">
                              {q.options.map((opt, oIdx) => {
                                const isSelected = userAnswers[q.question_id] === opt;
                                return (
                                  <label
                                    key={oIdx}
                                    className={`p-3 rounded-xl border flex items-center space-x-3 cursor-pointer transition-all text-xs ${
                                      isSelected
                                        ? 'bg-indigo-600/20 border-indigo-500 text-white font-bold'
                                        : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700'
                                    }`}
                                  >
                                    <input
                                      type="radio"
                                      name={`question_${q.question_id}`}
                                      value={opt}
                                      checked={isSelected}
                                      onChange={() => handleOptionSelect(q.question_id, opt)}
                                      className="hidden"
                                    />
                                    <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                                      isSelected ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
                                    }`}>
                                      {String.fromCharCode(65 + oIdx)}
                                    </span>
                                    <span>{opt}</span>
                                  </label>
                                );
                              })}
                            </div>
                          </div>
                        ))}
                      </div>

                      <button
                        onClick={handleSubmitQuiz}
                        disabled={Object.keys(userAnswers).length < quizQuestions.length || quizLoading}
                        className="w-full py-3.5 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-bold flex items-center justify-center space-x-2 shadow-lg shadow-emerald-600/20 transition-all disabled:opacity-50"
                      >
                        {quizLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <CheckCircle2 className="w-5 h-5" />}
                        <span>Submit Verification Answers</span>
                      </button>
                    </div>
                  )}

                  {/* QUIZ RESULT SCREEN */}
                  {quizResult && (
                    <div className="space-y-6 animate-fadeIn">
                      <div className={`p-6 rounded-3xl border text-center space-y-3 ${
                        quizResult.passed 
                          ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300' 
                          : 'bg-red-500/10 border-red-500/40 text-red-300'
                      }`}>
                        {quizResult.passed ? (
                          <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto" />
                        ) : (
                          <XCircle className="w-12 h-12 text-red-400 mx-auto" />
                        )}

                        <h3 className="text-xl font-extrabold text-white">
                          {quizResult.passed ? '✓ Learning Verified Successfully!' : '✗ Verification Not Passed'}
                        </h3>

                        <div className="flex justify-center items-center space-x-6 text-sm font-bold">
                          <div>
                            <span className="text-slate-400 block text-xs font-normal">Score</span>
                            <span className="text-2xl text-white">{quizResult.score} / {quizResult.total_questions}</span>
                          </div>
                          <div className="h-8 w-px bg-slate-800"></div>
                          <div>
                            <span className="text-slate-400 block text-xs font-normal">Percentage</span>
                            <span className="text-2xl text-white">{quizResult.percentage}%</span>
                          </div>
                        </div>

                        <p className="text-xs text-slate-300 max-w-md mx-auto">
                          {quizResult.message}
                        </p>
                      </div>

                      {/* Topic Performance Breakdown */}
                      {quizResult.topic_performance && (
                        <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                          <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-400">
                            Topic Performance Breakdown
                          </h4>
                          <div className="space-y-3">
                            {Object.entries(quizResult.topic_performance).map(([topic, pct]) => (
                              <div key={topic} className="space-y-1">
                                <div className="flex justify-between text-xs font-semibold">
                                  <span className="text-slate-300">{topic}</span>
                                  <span className={pct >= 70 ? 'text-emerald-400' : 'text-red-400'}>{pct}%</span>
                                </div>
                                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                                  <div 
                                    className={`h-full rounded-full ${pct >= 70 ? 'bg-emerald-400' : 'bg-red-400'}`}
                                    style={{ width: `${pct}%` }}
                                  ></div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Weak topics warning */}
                      {quizResult.weak_topics && quizResult.weak_topics.length > 0 && (
                        <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs space-y-1">
                          <span className="font-bold flex items-center space-x-1">
                            <AlertTriangle className="w-4 h-4 text-amber-400" />
                            <span>Recommended Topics to Review:</span>
                          </span>
                          <p className="text-slate-300">{quizResult.weak_topics.join(', ')}</p>
                        </div>
                      )}

                      <div className="flex items-center space-x-3">
                        {!quizResult.passed && (
                          <button
                            onClick={() => setActiveTab('learning')}
                            className="w-1/2 py-3 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all"
                          >
                            Review Topics
                          </button>
                        )}

                        <button
                          onClick={() => handleGenerateQuestions(selectedTask.id)}
                          className={`py-3 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center justify-center space-x-2 transition-all ${
                            quizResult.passed ? 'w-full' : 'w-1/2'
                          }`}
                        >
                          <RotateCcw className="w-4 h-4" />
                          <span>Generate NEW Questions (Retry)</span>
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 3: ATTEMPT HISTORY */}
              {activeTab === 'history' && (
                <div className="space-y-4">
                  {attemptHistory.length === 0 ? (
                    <div className="p-8 text-center text-slate-500 bg-slate-950/60 rounded-2xl border border-slate-800 text-xs">
                      No verification attempts recorded yet for this task.
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {attemptHistory.map((att) => (
                        <div key={att.id} className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 flex items-center justify-between">
                          <div className="space-y-1">
                            <div className="flex items-center space-x-2">
                              <span className="text-xs font-bold text-white">Attempt #{att.attempt_number}</span>
                              <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                att.passed ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-red-500/20 text-red-400 border border-red-500/30'
                              }`}>
                                {att.passed ? 'PASSED ✓' : 'FAILED ✗'}
                              </span>
                            </div>
                            <span className="text-[11px] text-slate-500 block">
                              Date: {att.created_at ? new Date(att.created_at).toLocaleString() : 'Recent'}
                            </span>
                          </div>

                          <div className="text-right">
                            <span className="text-base font-extrabold text-white">{att.percentage}%</span>
                            <span className="text-[11px] text-slate-400 block">{att.score} / {att.total_questions} Correct</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Roadmap;
