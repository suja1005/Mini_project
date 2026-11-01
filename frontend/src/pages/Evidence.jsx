import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { evidenceService } from '../services/evidenceService';
import PhaseBanner from '../components/PhaseBanner';
import MetricCard from '../components/MetricCard';
import { 
  ShieldCheck, 
  PlusCircle, 
  RefreshCw, 
  CheckCircle2, 
  AlertTriangle, 
  FolderGit2, 
  ExternalLink, 
  GitBranch, 
  X, 
  Loader2, 
  Info,
  Award,
  Layers,
  FileText,
  ArrowRight
} from 'lucide-react';

const Evidence = () => {
  const [loading, setLoading] = useState(true);
  const [recalculating, setRecalculating] = useState(false);
  const [overview, setOverview] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCertificateForm, setShowCertificateForm] = useState(false);
  const [selectedSkillNotes, setSelectedSkillNotes] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  // Project form state
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    skills_used: [],
    project_type: 'Capstone',
    completion_status: 'Completed',
    project_link: '',
    github_link: '',
    student_role: 'Full Stack Developer'
  });
  const [availableSkills] = useState([
    'Python', 'Java', 'C', 'C++', 'JavaScript', 'HTML', 'CSS', 'React',
    'SQL', 'MongoDB', 'Machine Learning', 'Data Analysis', 'Computer Networks',
    'Git', 'Problem Solving', 'Communication', 'Analytical Thinking', 'Aptitude'
  ]);
  const [savingProject, setSavingProject] = useState(false);
  const [savingCertificate, setSavingCertificate] = useState(false);
  const [certificateData, setCertificateData] = useState({
    title: '',
    issuer: '',
    skills: [],
    issue_date: '',
    credential_url: ''
  });

  const fetchEvidence = async () => {
    setLoading(true);
    try {
      const data = await evidenceService.getEvidence();
      setOverview(data);
    } catch (err) {
      console.error("Error fetching evidence:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvidence();
  }, []);

  const handleRecalculate = async () => {
    setRecalculating(true);
    try {
      const data = await evidenceService.recalculateEvidence();
      setOverview(data);
      setSuccessMessage("Evidence recalculated using latest assessment and project artifacts!");
      setTimeout(() => setSuccessMessage(''), 4000);
    } catch (err) {
      console.error("Error recalculating evidence:", err);
    } finally {
      setRecalculating(false);
    }
  };

  const handleSkillToggle = (skill) => {
    setFormData(prev => {
      const exists = prev.skills_used.includes(skill);
      return {
        ...prev,
        skills_used: exists 
          ? prev.skills_used.filter(s => s !== skill)
          : [...prev.skills_used, skill]
      };
    });
  };

  const handleSaveProject = async (e) => {
    e.preventDefault();
    if (!formData.title || formData.skills_used.length === 0) {
      alert("Please provide a project title and select at least one skill.");
      return;
    }

    setSavingProject(true);
    try {
      await evidenceService.addProjectEvidence(formData);
      setShowModal(false);
      setFormData({
        title: '',
        description: '',
        skills_used: [],
        project_type: 'Capstone',
        completion_status: 'Completed',
        project_link: '',
        github_link: '',
        student_role: 'Full Stack Developer'
      });
      setSuccessMessage("Project evidence successfully added and skill scores recalculated!");
      setTimeout(() => setSuccessMessage(''), 5000);
      await fetchEvidence();
    } catch (err) {
      console.error("Error adding project evidence:", err);
      alert("Failed to save project evidence. Please try again.");
    } finally {
      setSavingProject(false);
    }
  };

  const handleSaveCertificate = async (e) => {
    e.preventDefault();
    if (!certificateData.title.trim() || !certificateData.issuer.trim() || certificateData.skills.length === 0) {
      alert('Please provide a certificate title, issuer, and at least one related skill.');
      return;
    }
    setSavingCertificate(true);
    try {
      await evidenceService.addCertificateEvidence(certificateData);
      setCertificateData({ title: '', issuer: '', skills: [], issue_date: '', credential_url: '' });
      setShowCertificateForm(false);
      setSuccessMessage('Certificate evidence saved. Practical assessment is still required for skill verification.');
      setTimeout(() => setSuccessMessage(''), 5000);
      await fetchEvidence();
    } catch (err) {
      console.error('Error adding certificate evidence:', err);
      alert(err.response?.data?.detail || 'Failed to save certificate evidence. Please try again.');
    } finally {
      setSavingCertificate(false);
    }
  };

  const handleCertificateSkillToggle = (skill) => {
    setCertificateData((prev) => ({
      ...prev,
      skills: prev.skills.includes(skill)
        ? prev.skills.filter((item) => item !== skill)
        : [...prev.skills, skill]
    }));
  };

  if (loading) {
    return (
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Loading Employability Evidence Engine...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white flex items-center space-x-3">
            <ShieldCheck className="w-8 h-8 text-indigo-400" />
            <span>Employability Evidence Engine</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Empirical Skill Verification — Claimed Skill ≠ Verified Skill
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={handleRecalculate}
            disabled={recalculating}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold flex items-center space-x-2 transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${recalculating ? 'animate-spin' : ''}`} />
            <span>Recalculate Evidence</span>
          </button>
          <button
            onClick={() => setShowModal(true)}
            className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs flex items-center space-x-2 shadow-lg shadow-indigo-600/30 transition-all"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Add Project Evidence</span>
          </button>
          <button
            onClick={() => setShowCertificateForm((visible) => !visible)}
            className="px-4 py-2.5 rounded-xl bg-violet-700 hover:bg-violet-600 text-white font-semibold text-xs flex items-center space-x-2 shadow-lg shadow-violet-700/20 transition-all"
          >
            <Award className="w-4 h-4" />
            <span>Add Certificate</span>
          </button>
        </div>
      </div>

      <section className="glass-card rounded-3xl border border-slate-800 p-6 space-y-4">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2"><Award className="h-5 w-5 text-violet-400" /><h2 className="text-lg font-bold text-white">Certificate Evidence</h2></div>
          <span className="rounded-full border border-violet-200 bg-violet-50 px-3 py-1 text-[11px] text-violet-800">{overview?.certificates?.length || 0} submitted</span>
        </div>
        <p className="text-xs text-slate-400">Certificates support your evidence record but never verify practical skill on their own.</p>
        {showCertificateForm && (
          <form onSubmit={handleSaveCertificate} className="grid gap-3 rounded-2xl border border-violet-200 bg-violet-50 p-4 md:grid-cols-2">
            <input required minLength={2} placeholder="Certificate title" value={certificateData.title} onChange={(e) => setCertificateData({ ...certificateData, title: e.target.value })} className="rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white" />
            <input required minLength={2} placeholder="Issuing organization" value={certificateData.issuer} onChange={(e) => setCertificateData({ ...certificateData, issuer: e.target.value })} className="rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white" />
            <input type="month" aria-label="Issue month" value={certificateData.issue_date} onChange={(e) => setCertificateData({ ...certificateData, issue_date: e.target.value })} className="rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white" />
            <input type="url" placeholder="Credential URL (optional)" value={certificateData.credential_url} onChange={(e) => setCertificateData({ ...certificateData, credential_url: e.target.value })} className="rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white" />
            <div className="md:col-span-2">
              <p className="mb-2 text-[11px] font-semibold text-slate-300">Related skills</p>
              <div className="flex flex-wrap gap-2">{availableSkills.map((skill) => <button key={skill} type="button" onClick={() => handleCertificateSkillToggle(skill)} className={`rounded-full border px-3 py-1 text-[11px] ${certificateData.skills.includes(skill) ? 'border-violet-700 bg-violet-700 text-white' : 'border-violet-200 bg-violet-100 text-violet-800'}`}>{skill}</button>)}</div>
            </div>
            <div className="flex justify-end gap-2 md:col-span-2">
              <button type="button" onClick={() => setShowCertificateForm(false)} className="rounded-lg px-4 py-2 text-xs font-semibold text-violet-800">Cancel</button>
              <button disabled={savingCertificate} className="inline-flex items-center gap-2 rounded-lg bg-violet-700 px-4 py-2 text-xs font-bold text-white disabled:opacity-50">{savingCertificate ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}Save certificate</button>
            </div>
          </form>
        )}
        {overview?.certificates?.length ? (
          <div className="grid gap-3 md:grid-cols-2">
            {overview.certificates.map((certificate) => (
              <article key={certificate.id} className="rounded-xl border border-violet-200 bg-violet-50 p-4">
                <h3 className="font-bold text-white">{certificate.title}</h3>
                <p className="mt-1 text-xs text-slate-400">{certificate.issuer}{certificate.issue_date ? ` · ${certificate.issue_date}` : ''}</p>
                <div className="mt-2 flex flex-wrap gap-1">{certificate.skills.map((skill) => <span key={skill} className="rounded-full bg-violet-100 px-2 py-1 text-[10px] text-violet-800">{skill}</span>)}</div>
                {certificate.credential_url && <a href={certificate.credential_url} target="_blank" rel="noreferrer" className="mt-3 inline-flex items-center gap-1 text-[11px] font-semibold text-violet-300">Open credential <ExternalLink className="h-3 w-3" /></a>}
              </article>
            ))}
          </div>
        ) : <p className="rounded-xl bg-violet-50 p-4 text-xs text-violet-800">No certificate evidence submitted.</p>}
      </section>

      <PhaseBanner 
        title="Feature 4 — Transparent Dual-Factor Evidence Verification"
        message="Certificates and projects are supporting evidence—not proof of practical skill. Complete the next career-specific assessment to validate your claimed skills before your adaptive roadmap."
      />

      <div className="flex flex-col gap-3 rounded-2xl border border-violet-200 bg-violet-50 p-4 dark:border-violet-900/60 dark:bg-violet-950/25 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-bold text-violet-900 dark:text-violet-200">Next: validate your skills in practice</p>
          <p className="mt-1 text-xs text-violet-800 dark:text-violet-300">Your selected career and submitted evidence help tailor the questions.</p>
        </div>
        <Link to="/practical-assessment" className="inline-flex items-center justify-center gap-2 rounded-xl bg-violet-700 px-4 py-2.5 text-xs font-bold text-white hover:bg-violet-600">
          Continue to practical assessment <ArrowRight className="h-4 w-4" />
        </Link>
      </div>

      {successMessage && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center space-x-2 animate-fadeIn">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{successMessage}</span>
        </div>
      )}

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <MetricCard 
          title="Claimed Skills" 
          value={overview?.total_claimed || 0} 
          subtitle="Self-Declared in Profile" 
          icon={Layers} 
          color="indigo" 
        />
        <MetricCard 
          title="Fully Verified" 
          value={overview?.total_verified || 0} 
          subtitle="Dual-Factor Empirical Proof" 
          icon={Award} 
          color="emerald" 
        />
        <MetricCard 
          title="Partially Verified" 
          value={overview?.total_partially_verified || 0} 
          subtitle="Single-Source Evidence" 
          icon={AlertTriangle} 
          color="amber" 
        />
        <MetricCard 
          title="Average Confidence" 
          value={`${overview?.average_confidence || 0}%`} 
          subtitle={overview?.overall_evidence_status || 'Evaluating'} 
          icon={ShieldCheck} 
          color="cyan" 
        />
      </div>

      {/* Skills Verification Table */}
      <div className="glass-card rounded-3xl border border-slate-800 overflow-hidden">
        <div className="p-6 border-b border-slate-800 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white">My Skills Verification Status</h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Comparing self-declared proficiency vs objective assessment & project evidence
            </p>
          </div>
          <span className="text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
            {overview?.skills?.length || 0} Skills Monitored
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/80 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
              <tr>
                <th className="px-6 py-3.5">Skill</th>
                <th className="px-6 py-3.5">Claimed Level</th>
                <th className="px-6 py-3.5">Assessment Evidence</th>
                <th className="px-6 py-3.5">Project Evidence</th>
                <th className="px-6 py-3.5">Verified Score</th>
                <th className="px-6 py-3.5">Confidence</th>
                <th className="px-6 py-3.5">Evidence Status</th>
                <th className="px-6 py-3.5 text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {overview?.skills?.map((item) => (
                <tr key={item.skill} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4 font-bold text-white text-sm">
                    {item.skill}
                  </td>
                  <td className="px-6 py-4">
                    <span className="font-semibold text-slate-300">{item.claimed_level}</span>
                    <span className="text-slate-500 ml-1">({item.claimed_score} pts)</span>
                  </td>
                  <td className="px-6 py-4">
                    {item.assessment_score !== null ? (
                      <span className="font-semibold text-indigo-400">{item.assessment_score}%</span>
                    ) : (
                      <span className="text-slate-500 italic">No Assessment</span>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    {item.project_score !== null ? (
                      <span className="font-semibold text-emerald-400">{item.project_score}%</span>
                    ) : (
                      <span className="text-slate-500 italic">No Project</span>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-base font-extrabold text-indigo-300">{item.verified_score}</span>
                      <span className="text-[10px] text-slate-500">/ 100</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1.5">
                        <span className={`text-[11px] font-bold ${
                          item.confidence === 'HIGH' ? 'text-emerald-400' :
                          item.confidence === 'MEDIUM' ? 'text-amber-400' : 'text-rose-400'
                        }`}>
                          {item.confidence}
                        </span>
                        <span className="text-[10px] text-slate-400">({item.confidence_score}%)</span>
                      </div>
                      <div className="w-16 bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div 
                          className={`h-full rounded-full ${
                            item.confidence === 'HIGH' ? 'bg-emerald-500' :
                            item.confidence === 'MEDIUM' ? 'bg-amber-500' : 'bg-rose-500'
                          }`}
                          style={{ width: `${item.confidence_score}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-semibold border ${
                      item.status === 'VERIFIED'
                        ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                        : item.status === 'PARTIALLY VERIFIED'
                        ? 'bg-amber-500/15 text-amber-300 border-amber-500/30'
                        : 'bg-rose-500/15 text-rose-300 border-rose-500/30'
                    }`}>
                      {item.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => setSelectedSkillNotes(item)}
                      title="View Evidence Formula Details"
                      className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
                    >
                      <Info className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Submitted Project Evidence Section */}
      <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FolderGit2 className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-white">Student Project Evidence Artifacts</h2>
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center space-x-1"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span>Submit New Project</span>
          </button>
        </div>

        {overview?.projects?.length === 0 ? (
          <div className="p-8 text-center text-slate-500 bg-slate-900/40 rounded-2xl border border-slate-800 space-y-2">
            <FolderGit2 className="w-8 h-8 text-slate-600 mx-auto" />
            <p className="text-sm">No project evidence submitted yet.</p>
            <p className="text-xs text-slate-600">
              Submit your academic capstone, personal repo, or hackathon project to boost verified skills!
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {overview?.projects?.map((proj) => (
              <div key={proj.id} className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3 flex flex-col justify-between">
                <div>
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                        {proj.project_type}
                      </span>
                      <h3 className="text-base font-bold text-white mt-1.5">{proj.title}</h3>
                    </div>
                    <div className="text-right">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {proj.completion_status}
                      </span>
                      <div className="text-xs text-slate-400 mt-1 font-semibold">
                        Score: <span className="text-indigo-400">{proj.verified_score} pts</span>
                      </div>
                    </div>
                  </div>

                  <p className="text-xs text-slate-400 mt-2 line-clamp-2">{proj.description}</p>

                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {proj.skills_used?.map((sk, i) => (
                      <span key={i} className="px-2 py-0.5 rounded-lg bg-violet-700 text-white text-[10px] font-semibold border border-violet-700">
                        {sk}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-slate-800/80 text-xs">
                  <span className="text-slate-500 text-[11px]">Role: {proj.student_role}</span>
                  <div className="flex space-x-2">
                    {proj.github_link && (
                      <a 
                        href={proj.github_link} 
                        target="_blank" 
                        rel="noreferrer" 
                        className="text-slate-400 hover:text-white flex items-center space-x-1"
                      >
                        <GitBranch className="w-3.5 h-3.5" />
                        <span>GitHub</span>
                      </a>
                    )}
                    {proj.project_link && (
                      <a 
                        href={proj.project_link} 
                        target="_blank" 
                        rel="noreferrer" 
                        className="text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                        <span>Live</span>
                      </a>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Skill Notes Modal */}
      {selectedSkillNotes && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-card p-6 rounded-3xl border border-slate-800 max-w-md w-full space-y-4 animate-scaleUp">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <FileText className="w-5 h-5 text-indigo-400" />
                <span>{selectedSkillNotes.skill} Evidence Breakdown</span>
              </h3>
              <button 
                onClick={() => setSelectedSkillNotes(null)} 
                className="text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <div className="text-slate-400">Claimed Proficiency:</div>
                <div className="font-semibold text-white text-sm">
                  {selectedSkillNotes.claimed_level} ({selectedSkillNotes.claimed_score} pts)
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                  <div className="text-slate-400">Assessment Score:</div>
                  <div className="font-bold text-indigo-400 text-sm mt-0.5">
                    {selectedSkillNotes.assessment_score !== null ? `${selectedSkillNotes.assessment_score}%` : 'Pending'}
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                  <div className="text-slate-400">Project Score:</div>
                  <div className="font-bold text-emerald-400 text-sm mt-0.5">
                    {selectedSkillNotes.project_score !== null ? `${selectedSkillNotes.project_score}%` : 'None'}
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-indigo-950/30 border border-indigo-500/30 space-y-1.5">
                <div className="font-bold text-indigo-300">Verified Skill Score: {selectedSkillNotes.verified_score} / 100</div>
                <div className="text-[11px] text-slate-400">
                  Confidence: <span className="text-white font-semibold">{selectedSkillNotes.confidence} ({selectedSkillNotes.confidence_score}%)</span>
                </div>
                <div className="text-[11px] text-slate-400">
                  Status: <span className="text-emerald-400 font-semibold">{selectedSkillNotes.status}</span>
                </div>
              </div>

              <div>
                <div className="text-slate-300 font-bold mb-1.5">Evidence Notes & Explainability:</div>
                <ul className="space-y-1">
                  {selectedSkillNotes.evidence_notes?.map((note, idx) => (
                    <li key={idx} className="text-slate-400 flex items-start space-x-1.5">
                      <span className="text-indigo-400">•</span>
                      <span>{note}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button 
                onClick={() => setSelectedSkillNotes(null)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Project Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="glass-card p-6 md:p-8 rounded-3xl border border-slate-800 max-w-xl w-full space-y-5 my-8 animate-scaleUp">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                  <PlusCircle className="w-5 h-5 text-indigo-400" />
                  <span>Add Project Evidence</span>
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Submit practical artifacts to empirically verify your technical skills.
                </p>
              </div>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveProject} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-300 uppercase mb-1">Project Title *</label>
                <input 
                  type="text" 
                  required
                  placeholder="e.g. Real-time Disease Prediction Pipeline"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-300 uppercase mb-1">Description *</label>
                <textarea 
                  required
                  rows="3"
                  placeholder="Summarize the project problem statement, architecture, models used, and outcomes..."
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 resize-none"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-300 uppercase mb-1">Skills Used (Select all that apply) *</label>
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {availableSkills.map((sk) => {
                    const isSelected = formData.skills_used.includes(sk);
                    return (
                      <button
                        type="button"
                        key={sk}
                        onClick={() => handleSkillToggle(sk)}
                        className={`px-3 py-1 rounded-xl text-xs font-semibold border transition-all ${
                          isSelected 
                            ? 'bg-indigo-600 text-white border-indigo-500' 
                            : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                        }`}
                      >
                        {sk} {isSelected && '✓'}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-300 uppercase mb-1">Project Type</label>
                  <select 
                    value={formData.project_type}
                    onChange={(e) => setFormData({...formData, project_type: e.target.value})}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none"
                  >
                    <option value="Capstone">Final Year Capstone</option>
                    <option value="Academic">Academic Coursework</option>
                    <option value="Personal">Personal Portfolio</option>
                    <option value="Hackathon">Hackathon Submission</option>
                    <option value="Open Source">Open Source Contribution</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-300 uppercase mb-1">Completion Status</label>
                  <select 
                    value={formData.completion_status}
                    onChange={(e) => setFormData({...formData, completion_status: e.target.value})}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none"
                  >
                    <option value="Completed">Completed</option>
                    <option value="In Progress">In Progress</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-300 uppercase mb-1">GitHub Link (Optional)</label>
                  <input 
                    type="url" 
                    placeholder="https://github.com/user/repo"
                    value={formData.github_link}
                    onChange={(e) => setFormData({...formData, github_link: e.target.value})}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-300 uppercase mb-1">Live Demo Link (Optional)</label>
                  <input 
                    type="url" 
                    placeholder="https://myproject.demo.app"
                    value={formData.project_link}
                    onChange={(e) => setFormData({...formData, project_link: e.target.value})}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-300 uppercase mb-1">Your Role</label>
                <input 
                  type="text" 
                  placeholder="e.g. Lead Developer / ML Engineer"
                  value={formData.student_role}
                  onChange={(e) => setFormData({...formData, student_role: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                <button 
                  type="button" 
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white font-semibold"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  disabled={savingProject}
                  className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold flex items-center space-x-2 disabled:opacity-50"
                >
                  {savingProject ? <Loader2 className="w-4 h-4 animate-spin" /> : <ShieldCheck className="w-4 h-4" />}
                  <span>Save Evidence</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Evidence;
