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
  ArrowRight,
  Info
} from 'lucide-react';

const Roadmap = () => {
  const [loading, setLoading] = useState(true);
  const [updatingTaskId, setUpdatingTaskId] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [filterType, setFilterType] = useState('ALL');
  const [toastMessage, setToastMessage] = useState('');

  const fetchRoadmap = async () => {
    setLoading(true);
    try {
      const data = await roadmapService.getRoadmap();
      setRoadmap(data);
    } catch (err) {
      console.error("Error fetching roadmap:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, []);

  const handleStartTask = async (taskId) => {
    setUpdatingTaskId(taskId);
    try {
      const updated = await roadmapService.updateTaskStatus(taskId, 'IN PROGRESS');
      setRoadmap(updated);
    } catch (err) {
      console.error("Error starting task:", err);
    } finally {
      setUpdatingTaskId(null);
    }
  };

  const handleCompleteTask = async (taskId, taskTitle) => {
    setUpdatingTaskId(taskId);
    try {
      const updated = await roadmapService.completeTask(taskId);
      setRoadmap(updated);
      setToastMessage(`🎉 Task "${taskTitle}" completed! Empirical skill progress and employability recalculated, roadmap priorities adaptively updated.`);
      setTimeout(() => setToastMessage(''), 6000);
    } catch (err) {
      console.error("Error completing task:", err);
    } finally {
      setUpdatingTaskId(null);
    }
  };

  const handleRegenerateRoadmap = async () => {
    setLoading(true);
    try {
      const data = await roadmapService.generateRoadmap(roadmap?.career_id || 'ai-engineer');
      setRoadmap(data);
      setToastMessage("Personalized roadmap regenerated using current verified skill gap state!");
      setTimeout(() => setToastMessage(''), 5000);
    } catch (err) {
      console.error("Error regenerating roadmap:", err);
    } finally {
      setLoading(false);
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

  if (loading) {
    return (
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Generating Personalized Adaptive Roadmap...</span>
      </div>
    );
  }

  const tasks = roadmap?.tasks || [];
  const filteredTasks = tasks.filter(t => {
    if (filterType === 'ALL') return true;
    if (filterType === 'HIGH') return t.priority === 'HIGH';
    if (filterType === 'COMPLETED') return t.status === 'COMPLETED';
    if (filterType === 'PENDING') return t.status !== 'COMPLETED';
    return t.type.toLowerCase().includes(filterType.toLowerCase());
  });

  // Group filtered tasks by phase
  const groupedPhases = [1, 2, 3, 4, 5].map(phaseNum => {
    const phaseTasks = filteredTasks.filter(t => t.phase === phaseNum);
    const phaseName = roadmap?.phases?.[phaseNum - 1] || `Phase ${phaseNum}`;
    return { phaseNum, phaseName, tasks: phaseTasks };
  }).filter(g => g.tasks.length > 0);

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center space-x-3">
            <Map className="w-8 h-8 text-indigo-400" />
            <span>Adaptive Employability Roadmap</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Target Career: <span className="text-white font-bold">{roadmap?.career_title}</span> — Prioritized by Verified Skill Gaps
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={handleRegenerateRoadmap}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold flex items-center space-x-2 transition-all"
          >
            <RefreshCw className="w-4 h-4 text-indigo-400" />
            <span>Adapt Priorities</span>
          </button>
        </div>
      </div>

      <PhaseBanner 
        title="Feature 5 — Dynamic Adaptive Employability Roadmap"
        message="Roadmap tasks are individualized and adapt dynamically: completing an assessment or project improves your verified skill, shrinking the gap and shifting priorities."
      />

      {toastMessage && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center space-x-2 shadow-lg shadow-emerald-500/10 animate-fadeIn">
          <Sparkles className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Employability Metrics Header Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <MetricCard 
          title="Current Employability" 
          value={`${roadmap?.current_employability}%`} 
          subtitle="Model-based Estimate" 
          icon={TrendingUp} 
          color="emerald" 
        />
        <MetricCard 
          title="Target Employability" 
          value={`${roadmap?.target_employability}%`} 
          subtitle={`For ${roadmap?.career_title}`} 
          icon={Target} 
          color="indigo" 
        />
        <MetricCard 
          title="Employability Gap" 
          value={`${roadmap?.employability_gap}%`} 
          subtitle="Points to Target" 
          icon={TrendingUp} 
          color="amber" 
        />
        <MetricCard 
          title="Roadmap Progress" 
          value={`${roadmap?.progress_percentage}%`} 
          subtitle={`${roadmap?.completed_tasks} of ${roadmap?.total_tasks} Tasks Done`} 
          icon={CheckCircle2} 
          color="cyan" 
        />
      </div>

      {/* Progress Bar */}
      <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-2">
        <div className="flex justify-between text-xs font-semibold">
          <span className="text-slate-300">Overall Milestone Execution</span>
          <span className="text-indigo-400">{roadmap?.completed_tasks} / {roadmap?.total_tasks} Tasks Completed ({roadmap?.progress_percentage}%)</span>
        </div>
        <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
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
          { key: 'HIGH', label: 'High Priority Only' },
          { key: 'Learning', label: 'Learning Modules' },
          { key: 'Assessment', label: 'Assessments' },
          { key: 'Project', label: 'Applied Projects' },
          { key: 'PENDING', label: 'Pending' },
          { key: 'COMPLETED', label: 'Completed ✓' }
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
                  const isCompleted = task.status === 'COMPLETED';
                  const isInProgress = task.status === 'IN PROGRESS';
                  const isUpdating = updatingTaskId === task.id;

                  return (
                    <div 
                      key={task.id} 
                      className={`p-5 rounded-2xl border transition-all flex flex-col justify-between space-y-4 ${
                        isCompleted 
                          ? 'bg-slate-900/40 border-emerald-500/30 opacity-90'
                          : isInProgress
                          ? 'bg-slate-900/90 border-indigo-500/50 shadow-lg shadow-indigo-500/10'
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
                            <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                              task.priority === 'HIGH'
                                ? 'bg-red-500/15 text-red-400 border-red-500/30'
                                : task.priority === 'MEDIUM'
                                ? 'bg-amber-500/15 text-amber-400 border-amber-500/30'
                                : 'bg-slate-800 text-slate-400 border-slate-700'
                            }`}>
                              {task.priority} Priority
                            </span>
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              isCompleted 
                                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                                : isInProgress
                                ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 animate-pulse'
                                : 'bg-slate-800 text-slate-400'
                            }`}>
                              {task.status}
                            </span>
                          </div>
                        </div>

                        <div>
                          <h3 className={`text-base font-bold ${isCompleted ? 'text-slate-300 line-through decoration-emerald-500/60' : 'text-white'}`}>
                            {task.title}
                          </h3>
                          <p className="text-xs text-slate-400 mt-1">
                            {task.description}
                          </p>
                        </div>

                        {/* Explainability Accordion/Box */}
                        <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 text-[11px] text-slate-400 space-y-1">
                          <div className="flex items-center space-x-1 font-semibold text-slate-300">
                            <Info className="w-3 h-3 text-indigo-400" />
                            <span>Why is this prioritized?</span>
                          </div>
                          <p className="text-slate-400 leading-relaxed">
                            {task.explanation}
                          </p>
                        </div>

                        <div className="flex items-center space-x-4 text-xs text-slate-400 pt-1">
                          <span className="flex items-center space-x-1">
                            <Clock className="w-3.5 h-3.5 text-slate-500" />
                            <span>Effort: {task.estimated_effort}</span>
                          </span>
                          <span className="font-semibold text-indigo-400">
                            Skill: {task.skill}
                          </span>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                        <span className="text-[11px] text-slate-500">
                          {isCompleted ? 'Completed ✓' : isInProgress ? 'In Progress ⏳' : 'Not Started'}
                        </span>

                        <div className="flex space-x-2">
                          {!isCompleted && !isInProgress && (
                            <button
                              onClick={() => handleStartTask(task.id)}
                              disabled={isUpdating}
                              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold flex items-center space-x-1.5 transition-all disabled:opacity-50"
                            >
                              <Play className="w-3 h-3" />
                              <span>Start Task</span>
                            </button>
                          )}

                          {!isCompleted && (
                            <button
                              onClick={() => handleCompleteTask(task.id, task.title)}
                              disabled={isUpdating}
                              className="px-4 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center space-x-1.5 shadow-md shadow-emerald-600/20 transition-all disabled:opacity-50"
                            >
                              {isUpdating ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <CheckCircle2 className="w-3.5 h-3.5" />}
                              <span>Mark Complete</span>
                            </button>
                          )}

                          {isCompleted && (
                            <span className="text-xs text-emerald-400 font-bold flex items-center space-x-1">
                              <CheckCircle2 className="w-4 h-4" />
                              <span>Verified Completed</span>
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Roadmap;
