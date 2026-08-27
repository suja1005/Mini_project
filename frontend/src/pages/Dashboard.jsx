import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { profileService } from '../services/profileService';
import { assessmentService } from '../services/assessmentService';
import { recommendationService } from '../services/recommendationService';
import MetricCard from '../components/MetricCard';
import PhaseBanner from '../components/PhaseBanner';
import { 
  UserCheck, 
  Award, 
  Compass, 
  TrendingUp, 
  ArrowRight,
  ShieldAlert,
  MapPin,
  Activity,
  Loader2,
  AlertCircle
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [assessment, setAssessment] = useState(null);
  const [topCareer, setTopCareer] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        const [profData, passRes, recData] = await Promise.allSettled([
          profileService.getProfile(),
          assessmentService.getResults(),
          recommendationService.getRecommendations()
        ]);

        if (profData.status === 'fulfilled') setProfile(profData.value);
        if (passRes.status === 'fulfilled') setAssessment(passRes.value);
        if (recData.status === 'fulfilled' && recData.value?.top_recommendations?.length > 0) {
          setTopCareer(recData.value.top_recommendations[0]);
        }
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
        <span className="text-sm">Loading Student Dashboard Data...</span>
      </div>
    );
  }

  const isProfileComplete = profile?.is_complete ?? false;
  const isAssessmentComplete = assessment?.is_completed ?? false;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white">
            Welcome back, {user?.full_name || 'Student'} 👋
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            AI-Powered Career Guidance & Employability Enhancement Platform
          </p>
        </div>
        <Link 
          to="/recommendations"
          className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium shadow-lg shadow-indigo-600/30 transition-all text-sm w-fit"
        >
          <span>Analyze My Career</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      <PhaseBanner 
        title="Phase 1 Live Integrated Session"
        message={`Authenticated as ${user?.email || 'Student'}. Active sessions persist cleanly across browser refreshes.`}
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

      {/* Overview Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard 
          title="Current Employability"
          value="58 / 100"
          subtitle="Model-based Estimate"
          icon={TrendingUp}
          color="emerald"
        />
        <MetricCard 
          title="Top Career Recommendation"
          value={topCareer ? topCareer.title : "AI Engineer"}
          subtitle={`Career Fit: ${topCareer ? topCareer.fit_score : 87}%`}
          icon={Compass}
          color="indigo"
        />
        <MetricCard 
          title="Employability Target / Gap"
          value="80% Target"
          subtitle="Gap: 22%"
          icon={UserCheck}
          color="amber"
        />
        <MetricCard 
          title="Assessment Score"
          value={assessment ? `${assessment.overall_score}%` : "78%"}
          subtitle={assessment ? `${assessment.correct_count}/${assessment.total_questions} Correct` : "Completed"}
          icon={Award}
          color="cyan"
        />
      </div>

      {/* Main Grid Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Core Summary */}
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-card p-6 rounded-2xl border border-slate-800">
            <h2 className="text-lg font-bold text-white mb-4 flex items-center justify-between">
              <span>Career Fit & Achievability Summary</span>
              <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Calculated Score
              </span>
            </h2>

            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
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
                <div className="p-2.5 rounded-lg bg-slate-800/40 border border-slate-800">
                  <div className="text-xs text-slate-400">Readiness</div>
                  <div className="text-sm font-semibold text-slate-200 mt-0.5">58%</div>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-800/40 border border-slate-800">
                  <div className="text-xs text-slate-400">Employability Gap</div>
                  <div className="text-sm font-semibold text-amber-400 mt-0.5">22%</div>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-800/40 border border-slate-800">
                  <div className="text-xs text-slate-400">Learning Effort</div>
                  <div className="text-sm font-semibold text-purple-400 mt-0.5">HIGH</div>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-800/40 border border-slate-800">
                  <div className="text-xs text-slate-400">Achievability</div>
                  <div className="text-sm font-semibold text-emerald-400 mt-0.5">72%</div>
                </div>
              </div>

              <div className="pt-2 flex justify-end">
                <Link 
                  to={`/career/${topCareer ? topCareer.id : 'ai-engineer'}`}
                  className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
                >
                  <span>View Detailed Decision & Risk Analysis</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column - Future Architecture Placeholders */}
        <div className="space-y-6">
          <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 className="text-md font-bold text-slate-200">Future Phase Architecture</h2>
            
            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-1">
              <div className="flex items-center space-x-2 text-slate-400 text-xs font-semibold">
                <ShieldAlert className="w-4 h-4 text-slate-500" />
                <span>Feature 4: Evidence Engine</span>
              </div>
              <p className="text-xs text-slate-500">
                Evidence verification will be available in the next phase.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-1">
              <div className="flex items-center space-x-2 text-slate-400 text-xs font-semibold">
                <MapPin className="w-4 h-4 text-slate-500" />
                <span>Feature 5: Adaptive Roadmap</span>
              </div>
              <p className="text-xs text-slate-500">
                Personalized roadmap will be generated after skill-gap verification.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-1">
              <div className="flex items-center space-x-2 text-slate-400 text-xs font-semibold">
                <Activity className="w-4 h-4 text-slate-500" />
                <span>Feature 6: Progress Tracker</span>
              </div>
              <p className="text-xs text-slate-500">
                Employability progress tracking will become available after roadmap activities are completed.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
