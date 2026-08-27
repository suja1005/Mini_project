import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { profileService } from '../services/profileService';
import PhaseBanner from '../components/PhaseBanner';
import { UserCheck, CheckCircle2, ArrowRight, Save, Loader2 } from 'lucide-react';

const Onboarding = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  const [profileData, setProfileData] = useState({
    full_name: user?.full_name || '',
    degree: user?.degree || 'B.Tech',
    department: user?.department || 'Computer Science',
    year_of_study: 'Final Year',
    cgpa: '8.4 CGPA',
    technical_skills: {
      'Python': 85,
      'Machine Learning': 60,
      'SQL': 60,
      'Git': 70,
      'JavaScript': 60,
      'Data Analysis': 60
    },
    soft_skills: ['Communication', 'Problem Solving', 'Teamwork'],
    interests: ['Artificial Intelligence', 'Data Science', 'Software Development'],
    target_role: 'AI Engineer',
    preferred_domain: 'Artificial Intelligence'
  });

  useEffect(() => {
    const loadProfile = async () => {
      setLoading(true);
      try {
        const p = await profileService.getProfile();
        if (p) {
          setProfileData(prev => ({
            ...prev,
            ...p,
            full_name: p.full_name || user?.full_name || prev.full_name,
            degree: p.degree || user?.degree || prev.degree,
            department: p.department || user?.department || prev.department
          }));
        }
      } catch (err) {
        console.error("Error loading profile:", err);
      } finally {
        setLoading(false);
      }
    };
    loadProfile();
  }, [user]);

  const handleSkillChange = (skill, levelScore) => {
    setProfileData(prev => ({
      ...prev,
      technical_skills: {
        ...prev.technical_skills,
        [skill]: parseInt(levelScore, 10)
      }
    }));
  };

  const handleSaveProfile = async () => {
    setSaving(true);
    setSavedSuccess(false);
    try {
      await profileService.updateProfile(profileData);
      setSavedSuccess(true);
    } catch (err) {
      console.error("Error saving profile:", err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Loading Student Profile Data...</span>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-3">
            <UserCheck className="w-7 h-7 text-indigo-400" />
            <span>AI Student Profile Onboarding</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Build your comprehensive academic, technical, soft skills, and interest profile.
          </p>
        </div>
        <div className="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold border border-indigo-500/20">
          Module B Connected
        </div>
      </div>

      <PhaseBanner 
        title="Module B — AI Student Profile Data Persistence"
        message="Changes saved here are stored directly in your MongoDB student profile document."
      />

      {savedSuccess && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Profile successfully updated in MongoDB database!</span>
          </div>
          <button 
            onClick={() => navigate('/assessment')} 
            className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs flex items-center space-x-1"
          >
            <span>Continue to Assessment</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      <div className="glass-card p-6 md:p-8 rounded-3xl border border-slate-800 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex space-x-6 text-sm font-semibold">
            <span className={step >= 1 ? "text-indigo-400" : "text-slate-500"}>1. Academic Details</span>
            <span className={step >= 2 ? "text-indigo-400" : "text-slate-500"}>2. Technical Skills</span>
            <span className={step >= 3 ? "text-indigo-400" : "text-slate-500"}>3. Goals & Interests</span>
          </div>
          <span className="text-xs text-slate-400 font-mono">Step {step} of 3</span>
        </div>

        {step === 1 && (
          <div className="space-y-4">
            <h3 className="text-md font-bold text-slate-200">Academic Background</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Full Name</label>
                <input 
                  type="text" 
                  value={profileData.full_name} 
                  onChange={(e) => setProfileData({...profileData, full_name: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500" 
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Degree Program</label>
                <input 
                  type="text" 
                  value={profileData.degree} 
                  onChange={(e) => setProfileData({...profileData, degree: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500" 
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Department</label>
                <input 
                  type="text" 
                  value={profileData.department} 
                  onChange={(e) => setProfileData({...profileData, department: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500" 
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Year of Study</label>
                <select 
                  value={profileData.year_of_study}
                  onChange={(e) => setProfileData({...profileData, year_of_study: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500"
                >
                  <option value="Final Year">Final Year (Year 4)</option>
                  <option value="Third Year">Third Year (Year 3)</option>
                  <option value="Second Year">Second Year (Year 2)</option>
                </select>
              </div>
            </div>
            <div className="flex justify-end pt-4">
              <button 
                onClick={() => setStep(2)}
                className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center space-x-2"
              >
                <span>Next: Technical Skill Mapping</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <h3 className="text-md font-bold text-slate-200">Technical Skill Mapping</h3>
            <p className="text-xs text-slate-400">Skill level mapped values: Beginner (30), Intermediate (60), Advanced (85)</p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {['Python', 'Java', 'JavaScript', 'HTML/CSS', 'SQL', 'Git', 'Machine Learning', 'Data Analysis'].map((skill) => (
                <div key={skill} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                  <span className="text-sm font-semibold text-slate-200">{skill}</span>
                  <select 
                    value={profileData.technical_skills[skill] || 60}
                    onChange={(e) => handleSkillChange(skill, e.target.value)}
                    className="bg-slate-800 text-xs text-indigo-300 rounded-lg px-2.5 py-1.5 border border-slate-700 focus:outline-none"
                  >
                    <option value="85">Advanced (85)</option>
                    <option value="60">Intermediate (60)</option>
                    <option value="30">Beginner (30)</option>
                  </select>
                </div>
              ))}
            </div>

            <div className="flex justify-between pt-4">
              <button onClick={() => setStep(1)} className="px-4 py-2 text-slate-400 hover:text-white text-sm font-semibold">Back</button>
              <button onClick={() => setStep(3)} className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center space-x-2">
                <span>Next: Goals & Interests</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <h3 className="text-md font-bold text-slate-200">Career Goals & Preferred Domain</h3>
            <div className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Target Role</label>
                <input 
                  type="text" 
                  value={profileData.target_role}
                  onChange={(e) => setProfileData({...profileData, target_role: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500" 
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Interest Domains</label>
                <div className="flex flex-wrap gap-2 pt-1">
                  {profileData.interests.map((interest, i) => (
                    <span key={i} className="px-3 py-1.5 rounded-xl bg-indigo-600/20 text-indigo-300 text-xs font-semibold border border-indigo-500/30 flex items-center space-x-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400" />
                      <span>{interest}</span>
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between pt-6 border-t border-slate-800">
              <button onClick={() => setStep(2)} className="px-4 py-2 text-slate-400 hover:text-white text-sm font-semibold">Back</button>

              <div className="flex space-x-3">
                <button 
                  onClick={handleSaveProfile}
                  disabled={saving}
                  className="px-5 py-2.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 font-semibold text-sm border border-indigo-500/30 flex items-center space-x-2 disabled:opacity-50"
                >
                  {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                  <span>Save Profile</span>
                </button>

                <button 
                  onClick={async () => {
                    await handleSaveProfile();
                    navigate('/assessment');
                  }}
                  className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm flex items-center space-x-2"
                >
                  <span>Continue to Assessment</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Onboarding;
