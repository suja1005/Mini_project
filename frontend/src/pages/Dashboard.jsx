import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
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
  ArrowUpRight
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [assessment, setAssessment] = useState(null);
  const [topCareer, setTopCareer] = useState(null);
  const [evidence, setEvidence] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [progress, setProgress] = useState(null);

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

  if (loading) {
    return (
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Loading Student Dashboard & Evidence State...</span>
      </div>
    );
  }

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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white">
            Welcome back, {user?.full_name || 'Student'} 👋
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            AI-Powered Career Guidance & Employability Enhancement Platform — Phase 2 Active
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Link 
            to="/roadmap"
            className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold shadow-lg shadow-indigo-600/30 transition-all text-sm w-fit"
          >
            <Sparkles className="w-4 h-4" />
            <span>Continue Roadmap</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      <PhaseBanner 
        title="Phase 2 Integrated Platform Active"
        message="Evidence-Based Employability Enhancement Engine is online. Verified skills dynamically govern career readiness, adaptive roadmaps, and progress tracking."
      />

      {/* Completion Banners / Empty States */}
      {(!isProfileComplete || !isAssessmentComplete) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {!isProfileComplete && (
            <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <AlertCircle className="w-5 h-5 text-amber-400 shrink-0" />
                <div className="text-xs text-amber-200">
                  <span className="font-bold block text-sm">Profile Incomplete</span>
                  Complete your AI profile to unlock personalized recommendations.
                </div>
              </div>
              <Link to="/profile" className="px-3.5 py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded-lg text-xs shrink-0">
                Complete Profile
              </Link>
            </div>
          )}

          {!isAssessmentComplete && (
            <div className="p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <AlertCircle className="w-5 h-5 text-indigo-400 shrink-0" />
                <div className="text-xs text-indigo-200">
                  <span className="font-bold block text-sm">Assessment Pending</span>
                  Take the skill assessment to verify logical & technical score.
                </div>
              </div>
              <Link to="/assessment" className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs shrink-0">
                Take Assessment
              </Link>
            </div>
          )}
        </div>
      )}

      {/* Phase 2 Enhanced Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <MetricCard 
          title="Current Employability"
          value={`${currentEmp}%`}
          subtitle={`Target: ${targetEmp}%`}
          icon={TrendingUp}
          color="emerald"
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
          title="Completed Tasks"
          value={`${completedTasks}`}
          subtitle={progress?.improvement_delta > 0 ? `+${progress?.improvement_delta}% Employability gain` : "Active Execution"}
          icon={CheckCircle2}
          color="emerald"
        />
      </div>

      {/* Main Grid Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Core Summary */}
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-card p-6 rounded-3xl border border-slate-800">
            <h2 className="text-lg font-bold text-white mb-4 flex items-center justify-between">
              <span>Career Fit & Achievability Summary</span>
              <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Verified Model
              </span>
            </h2>

            <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-300 font-medium">Top Match: {topCareer ? topCareer.title : "AI Engineer"}</span>
                <span className="text-indigo-400 font-bold text-base">{topCareer ? topCareer.fit_score : 87}% Fit</span>
              </div>
              
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-full rounded-full transition-all"
                  style={{ width: `${topCareer ? topCareer.fit_score : 87}%` }}
                ></div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-center">
                <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800">
                  <div className="text-xs text-slate-400">Current Readiness</div>
                  <div className="text-sm font-bold text-emerald-400 mt-0.5">{currentEmp}%</div>
                </div>
                <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800">
                  <div className="text-xs text-slate-400">Employability Gap</div>
                  <div className="text-sm font-bold text-amber-400 mt-0.5">{empGap}%</div>
                </div>
                <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800">
                  <div className="text-xs text-slate-400">Verified Skills</div>
                  <div className="text-sm font-bold text-indigo-300 mt-0.5">{evidence?.total_verified || 0} Fully Proven</div>
                </div>
                <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800">
                  <div className="text-xs text-slate-400">Roadmap Tasks</div>
                  <div className="text-sm font-bold text-cyan-400 mt-0.5">{completedTasks}/{totalTasks} Done</div>
                </div>
              </div>

              <div className="pt-2 flex justify-between items-center text-xs">
                <Link 
                  to="/evidence"
                  className="text-slate-400 hover:text-white flex items-center space-x-1 font-semibold"
                >
                  <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Review Evidence Breakdown</span>
                </Link>

                <Link 
                  to={`/career/${topCareer ? topCareer.id : 'ai-engineer'}`}
                  className="font-semibold text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
                >
                  <span>Decision & Risk Details</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </div>

          {/* Active Next Task Card */}
          {nextTask && (
            <div className="glass-card p-6 rounded-3xl border border-indigo-500/30 bg-indigo-950/20 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Sparkles className="w-5 h-5 text-indigo-400" />
                  <h3 className="text-base font-bold text-white">Next Priority Roadmap Action</h3>
                </div>
                <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold border ${
                  nextTask.priority === 'HIGH' ? 'bg-red-500/20 text-red-400 border-red-500/30' : 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                }`}>
                  {nextTask.priority} Priority
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-indigo-300">{nextTask.type} • {nextTask.skill}</span>
                  <span className="text-[11px] text-slate-500">Effort: {nextTask.estimated_effort}</span>
                </div>
                <h4 className="text-base font-bold text-white">{nextTask.title}</h4>
                <p className="text-xs text-slate-400 line-clamp-2">{nextTask.description}</p>
              </div>

              <div className="flex justify-end">
                <Link
                  to="/roadmap"
                  className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center space-x-2 shadow-lg shadow-indigo-600/30 transition-all"
                >
                  <span>Continue Roadmap</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          )}
        </div>

        {/* Right Column - Live Phase 2 Enhancement Modules */}
        <div className="space-y-6">
          <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
            <h2 className="text-base font-bold text-white flex items-center space-x-2">
              <span>Enhancement Modules</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Phase 2
              </span>
            </h2>
            
            {/* Feature 4: Evidence Engine */}
            <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Evidence Engine</span>
                </div>
                <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  {evidence?.overall_evidence_status || 'Active'}
                </span>
              </div>
              <p className="text-xs text-slate-400">
                {evidence?.total_verified || 0} skills dual-verified with {evidence?.projects?.length || 0} project artifacts submitted.
              </p>
              <Link 
                to="/evidence" 
                className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center space-x-1 pt-1"
              >
                <span>Verify Skills & Add Projects</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {/* Feature 5: Adaptive Roadmap */}
            <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-emerald-400 text-xs font-bold">
                  <Map className="w-4 h-4" />
                  <span>Adaptive Roadmap</span>
                </div>
                <span className="text-[10px] font-bold text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                  {progressPct}% Done
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Prioritized tasks adapt automatically when you complete assessments or projects.
              </p>
              <Link 
                to="/roadmap" 
                className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center space-x-1 pt-1"
              >
                <span>Open Personalized Roadmap</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {/* Feature 6: Progress Tracker */}
            <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-cyan-400 text-xs font-bold">
                  <BarChart3 className="w-4 h-4" />
                  <span>Progress Tracker</span>
                </div>
                <span className="text-[10px] font-bold text-cyan-300 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
                  {progress?.improvement_delta >= 0 ? `+${progress?.improvement_delta}% gain` : 'Tracking'}
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Longitudinal scoring history and skill progression bars over time.
              </p>
              <Link 
                to="/progress" 
                className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 flex items-center space-x-1 pt-1"
              >
                <span>View Historical Trends</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
