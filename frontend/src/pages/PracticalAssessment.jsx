import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight, Award, CheckCircle2, Clock3, Code2, FileCheck2, Loader2,
  MessageSquareText, RotateCcw, ShieldCheck, Sparkles, Target, TriangleAlert
} from 'lucide-react';
import { practicalAssessmentService } from '../services/practicalAssessmentService';

const categoryStyles = {
  Weak: 'text-rose-700 bg-rose-50 border-rose-200 dark:text-rose-300 dark:bg-rose-950/30 dark:border-rose-900',
  'Needs Improvement': 'text-amber-700 bg-amber-50 border-amber-200 dark:text-amber-300 dark:bg-amber-950/30 dark:border-amber-900',
  Good: 'text-blue-700 bg-blue-50 border-blue-200 dark:text-blue-300 dark:bg-blue-950/30 dark:border-blue-900',
  Strong: 'text-emerald-700 bg-emerald-50 border-emerald-200 dark:text-emerald-300 dark:bg-emerald-950/30 dark:border-emerald-900'
};

const formatTime = (seconds) => `${Math.floor(seconds / 60).toString().padStart(2, '0')}:${(seconds % 60).toString().padStart(2, '0')}`;

const PracticalAssessment = () => {
  const [status, setStatus] = useState(null);
  const [history, setHistory] = useState([]);
  const [assessment, setAssessment] = useState(null);
  const [result, setResult] = useState(null);
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [remainingSeconds, setRemainingSeconds] = useState(1800);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const loadPage = async () => {
    try {
      const [assessmentStatus, attempts] = await Promise.all([
        practicalAssessmentService.getStatus(),
        practicalAssessmentService.getHistory()
      ]);
      setStatus(assessmentStatus);
      setHistory(attempts);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Unable to load your practical assessment.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadPage(); }, []);

  useEffect(() => {
    if (!assessment || result) return undefined;
    const timer = window.setInterval(() => {
      setRemainingSeconds((value) => Math.max(0, value - 1));
    }, 1000);
    return () => window.clearInterval(timer);
  }, [assessment, result]);

  const question = assessment?.questions?.[currentQuestion];
  const answeredCount = useMemo(() => Object.keys(answers).length, [answers]);
  const isComplete = assessment && answeredCount === assessment.total_questions;

  const startAssessment = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    setAnswers({});
    setCurrentQuestion(0);
    try {
      const next = await practicalAssessmentService.start();
      setAssessment(next);
      setRemainingSeconds(next.time_limit_minutes * 60);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Unable to generate your assessment.');
    } finally {
      setLoading(false);
    }
  };

  const submitAssessment = async () => {
    if (!assessment || submitting) return;
    if (answeredCount !== assessment.total_questions) {
      setError('Answer every question before submitting your assessment.');
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      const submission = await practicalAssessmentService.submit(assessment.assessment_id, answers);
      setResult(submission);
      setAssessment(null);
      const [nextStatus, attempts] = await Promise.all([
        practicalAssessmentService.getStatus(),
        practicalAssessmentService.getHistory()
      ]);
      setStatus(nextStatus);
      setHistory(attempts);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Unable to submit your answers.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading && !assessment && !result && !status) {
    return <div className="min-h-[55vh] grid place-items-center text-slate-500"><Loader2 className="animate-spin text-violet-600" /></div>;
  }

  const visibleResults = result?.skill_results || status?.skill_results || [];
  const visiblePlan = result?.adaptive_roadmap || status?.adaptive_roadmap || [];
  const claimedSkills = result?.claimed_skills || status?.claimed_skills || [];
  const verifiedSkills = result?.verified_skills || status?.verified_skills || [];
  const improvementSkills = result?.skills_needing_improvement || status?.skills_needing_improvement || [];
  const evidence = result?.evidence_submitted || status?.evidence_submitted || { projects: 0, certificates: 0 };

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-16">
      <header className="assessment-header rounded-3xl border border-violet-100 dark:border-violet-900/50 bg-gradient-to-br from-white to-violet-50 dark:from-slate-900 dark:to-violet-950/30 p-6 md:p-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">
          <div>
            <div className="assessment-header-copy flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-white">
              <ShieldCheck className="w-4 h-4" /> Evidence → practical validation
            </div>
            <h1 className="assessment-header-copy mt-2 text-2xl md:text-3xl font-black text-white">Practical Skill Assessment</h1>
            <p className="assessment-header-copy mt-2 max-w-2xl text-sm text-white">
              Career-specific questions are selected from your claimed skills, evidence, and career requirements. Your score is calculated and saved securely by the backend.
            </p>
          </div>
          {assessment ? (
            <div className={`inline-flex items-center gap-2 rounded-xl border px-4 py-3 font-bold ${remainingSeconds < 120 ? 'border-rose-300 bg-rose-50 text-rose-700' : 'border-violet-200 bg-white text-violet-700 dark:bg-slate-900 dark:text-violet-300'}`}>
              <Clock3 className="w-4 h-4" /> {formatTime(remainingSeconds)}
            </div>
          ) : !result && (
            <button onClick={startAssessment} disabled={loading} className="inline-flex items-center justify-center gap-2 rounded-xl bg-violet-700 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-violet-700/20 hover:bg-violet-600 disabled:opacity-50">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Target className="w-4 h-4" />}
              {status?.has_completed ? 'Retake assessment' : 'Start practical assessment'}
            </button>
          )}
        </div>
        <div className="mt-5 grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          <div className="rounded-xl border border-violet-300 bg-violet-700 p-3 dark:border-violet-300 dark:bg-violet-700"><span className="text-white">Career</span><p className="mt-1 font-bold text-white">{assessment?.career_title || result?.career_title || status?.career_title || 'Not selected'}</p></div>
          <div className="rounded-xl border border-violet-300 bg-violet-700 p-3 dark:border-violet-300 dark:bg-violet-700"><span className="text-white">Claimed skills</span><p className="mt-1 font-bold text-white">{claimedSkills.length}</p></div>
          <div className="rounded-xl border border-violet-300 bg-violet-700 p-3 dark:border-violet-300 dark:bg-violet-700"><span className="text-white">Projects submitted</span><p className="mt-1 font-bold text-white">{evidence.projects}</p></div>
          <div className="rounded-xl border border-violet-300 bg-violet-700 p-3 dark:border-violet-300 dark:bg-violet-700"><span className="text-white">Certificates submitted</span><p className="mt-1 font-bold text-white">{evidence.certificates}</p></div>
        </div>
      </header>

      {error && <div role="alert" className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700 dark:border-rose-900 dark:bg-rose-950/30 dark:text-rose-300">{error}</div>}

      {assessment && question && (
        <section className="rounded-3xl border border-slate-200 bg-white p-5 md:p-7 dark:border-slate-800 dark:bg-slate-900">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="flex flex-wrap gap-2">
                <span className="rounded-full bg-violet-100 px-2.5 py-1 text-[11px] font-bold text-violet-700 dark:bg-violet-950 dark:text-violet-300">{question.skill}</span>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300">{question.difficulty}</span>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300">{question.topic}</span>
              </div>
              <p className="mt-3 text-xs text-slate-500">Question {currentQuestion + 1} of {assessment.total_questions}</p>
            </div>
            <span className="text-xs font-bold text-violet-700 dark:text-violet-300">{answeredCount} answered</span>
          </div>
          <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
            <div className="h-full rounded-full bg-violet-600 transition-all" style={{ width: `${((currentQuestion + 1) / assessment.total_questions) * 100}%` }} />
          </div>
          <h2 className="mt-6 whitespace-pre-wrap text-lg font-bold leading-relaxed text-slate-900 dark:text-white">{question.question}</h2>
          {question.type === 'mcq' ? (
            <div className="mt-5 grid gap-3">
              {question.options.map((option, index) => (
                <button key={`${question.question_id}-${index}`} onClick={() => setAnswers((prev) => ({ ...prev, [question.question_id]: option }))} className={`rounded-xl border px-4 py-3 text-left text-sm transition ${answers[question.question_id] === option ? 'border-violet-500 bg-violet-50 text-violet-900 dark:bg-violet-950/40 dark:text-violet-100' : 'border-slate-200 text-slate-700 hover:border-violet-300 dark:border-slate-700 dark:text-slate-200'}`}>
                  <span className="mr-3 inline-grid h-6 w-6 place-items-center rounded-full bg-slate-100 text-xs font-bold dark:bg-slate-800">{String.fromCharCode(65 + index)}</span>{option}
                </button>
              ))}
            </div>
          ) : (
            <label className="mt-5 block">
              <span className="mb-2 flex items-center gap-2 text-xs font-semibold text-slate-600 dark:text-slate-300"><Code2 className="w-4 h-4" /> Enter your answer</span>
              <textarea value={answers[question.question_id] || ''} onChange={(event) => setAnswers((prev) => ({ ...prev, [question.question_id]: event.target.value }))} rows={4} className="w-full rounded-xl border border-slate-200 bg-white p-3 font-mono text-sm text-slate-900 outline-none focus:border-violet-500 dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </label>
          )}
          <div className="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex flex-wrap gap-2">
              <button onClick={() => setCurrentQuestion((value) => Math.max(0, value - 1))} disabled={currentQuestion === 0} className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-bold text-slate-600 disabled:opacity-40 dark:border-slate-700 dark:text-slate-300">Previous</button>
              <button onClick={() => setCurrentQuestion((value) => Math.min(assessment.total_questions - 1, value + 1))} disabled={currentQuestion === assessment.total_questions - 1} className="rounded-lg border border-violet-200 px-4 py-2 text-xs font-bold text-violet-700 disabled:opacity-40 dark:border-violet-900 dark:text-violet-300">Next question</button>
            </div>
            {remainingSeconds === 0 ? (
              <button onClick={startAssessment} className="inline-flex items-center justify-center gap-2 rounded-xl bg-rose-700 px-5 py-3 text-xs font-bold text-white">Time expired — restart</button>
            ) : (
              <button onClick={submitAssessment} disabled={!isComplete || submitting} className="inline-flex items-center justify-center gap-2 rounded-xl bg-violet-700 px-5 py-3 text-xs font-bold text-white hover:bg-violet-600 disabled:cursor-not-allowed disabled:opacity-45">
              {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />} Submit assessment
              </button>
            )}
          </div>
          {!isComplete && <p className="mt-2 text-right text-[11px] text-slate-500">Answer all {assessment.total_questions} questions to submit.</p>}
          <div className="mt-5 flex flex-wrap gap-2 border-t border-slate-100 pt-4 dark:border-slate-800">
            {assessment.questions.map((item, index) => (
              <button key={item.question_id} onClick={() => setCurrentQuestion(index)} aria-label={`Go to question ${index + 1}`} className={`h-8 w-8 rounded-lg text-xs font-bold ${index === currentQuestion ? 'bg-violet-700 text-white' : answers[item.question_id] !== undefined ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 text-slate-500 dark:bg-slate-800'}`}>{index + 1}</button>
            ))}
          </div>
        </section>
      )}

      {(result || status?.has_completed) && !assessment && (
        <>
          {result && (
            <div className="flex flex-col gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 p-5 dark:border-emerald-900 dark:bg-emerald-950/30 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-3"><Award className="h-6 w-6 text-emerald-600 dark:text-emerald-300" /><div><p className="font-bold text-emerald-900 dark:text-emerald-200">Assessment submitted</p><p className="text-xs text-emerald-800 dark:text-emerald-300">Your skill profile and personalized learning priorities have been updated.</p></div></div>
              <div className="flex flex-wrap items-center gap-3">
                <span className="text-sm font-black text-emerald-800 dark:text-emerald-200">{result.overall_score}% overall</span>
                <Link to="/roadmap" className="inline-flex items-center justify-center gap-2 rounded-xl bg-violet-700 px-4 py-2.5 text-xs font-bold text-white">Open personalized roadmap <ArrowRight className="w-4 h-4" /></Link>
              </div>
            </div>
          )}

          <section className="rounded-3xl border border-slate-200 bg-white p-5 md:p-7 dark:border-slate-800 dark:bg-slate-900">
            <div className="flex items-center gap-2"><Target className="h-5 w-5 text-violet-600" /><h2 className="text-lg font-extrabold text-slate-900 dark:text-white">Skill-wise performance</h2></div>
            <p className="mt-1 text-xs text-slate-500">Weak 0–49% · Needs Improvement 50–69% · Good 70–84% · Strong 85–100%</p>
            <div className="mt-5 grid gap-3 md:grid-cols-2">
              {visibleResults.map((item) => (
                <article key={item.skill} className="rounded-2xl border border-slate-200 p-4 dark:border-slate-800">
                  <div className="flex items-start justify-between gap-3">
                    <div><h3 className="font-bold text-slate-900 dark:text-white">{item.skill}</h3><span className={`mt-1 inline-flex rounded-full border px-2 py-0.5 text-[10px] font-bold ${categoryStyles[item.category] || categoryStyles.Good}`}>{item.category}</span></div>
                    <span className="text-xl font-black text-violet-700 dark:text-violet-300">{item.score}%</span>
                  </div>
                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800"><div className={`h-full rounded-full ${item.score < 50 ? 'bg-rose-500' : item.score < 70 ? 'bg-amber-500' : item.score < 85 ? 'bg-blue-500' : 'bg-emerald-500'}`} style={{ width: `${item.score}%` }} /></div>
                  <div className="mt-2 flex flex-wrap justify-between gap-2 text-[11px] text-slate-500"><span>{item.correct_count}/{item.total_questions} correct</span><span>{item.verified ? 'Practically verified' : 'Assessed, not yet verified'}</span></div>
                </article>
              ))}
            </div>
          </section>

          <section className="grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
              <h2 className="flex items-center gap-2 font-bold text-slate-900 dark:text-white"><FileCheck2 className="h-4 w-4 text-violet-600" /> Evidence and verification</h2>
              <div className="mt-3 space-y-2 text-xs">
                <p className="flex justify-between gap-3"><span className="text-slate-500">Claimed skills</span><span className="text-right font-semibold text-slate-800 dark:text-slate-200">{claimedSkills.join(', ') || 'None'}</span></p>
                <p className="flex justify-between gap-3"><span className="text-slate-500">Evidence submitted</span><span className="font-semibold text-slate-800 dark:text-slate-200">{evidence.projects} projects · {evidence.certificates} certificates</span></p>
                <p className="flex justify-between gap-3"><span className="text-slate-500">Practically assessed</span><span className="text-right font-semibold text-slate-800 dark:text-slate-200">{visibleResults.map((item) => item.skill).join(', ') || 'None'}</span></p>
                <p className="flex justify-between gap-3"><span className="text-slate-500">Verified</span><span className="text-right font-semibold text-emerald-700 dark:text-emerald-300">{verifiedSkills.join(', ') || 'None yet'}</span></p>
                <p className="flex justify-between gap-3"><span className="text-slate-500">Needs improvement</span><span className="text-right font-semibold text-rose-700 dark:text-rose-300">{improvementSkills.join(', ') || 'None'}</span></p>
              </div>
              <p className="mt-3 flex items-start gap-2 rounded-lg bg-amber-50 p-3 text-[11px] text-amber-800 dark:bg-amber-950/30 dark:text-amber-300"><TriangleAlert className="h-4 w-4 shrink-0" /> Certificates and project records are evidence, not proof of practical skill by themselves.</p>
            </div>
            <div className="rounded-2xl border border-violet-100 bg-violet-50/60 p-5 dark:border-violet-900/50 dark:bg-violet-950/20">
              <h2 className="flex items-center gap-2 font-bold text-slate-900 dark:text-white"><Sparkles className="h-4 w-4 text-violet-600" /> Roadmap priorities</h2>
              {visiblePlan.length ? <ol className="mt-3 space-y-2">{visiblePlan.map((item, index) => <li key={item.skill} className="flex items-center gap-3 rounded-xl bg-white p-3 text-xs dark:bg-slate-900"><span className="grid h-6 w-6 place-items-center rounded-full bg-violet-100 font-bold text-violet-700 dark:bg-violet-950 dark:text-violet-300">{index + 1}</span><span className="font-semibold text-slate-800 dark:text-slate-200">{item.skill}</span><span className="ml-auto text-rose-600 dark:text-rose-300">{item.score}% · {item.priority}</span></li>)}</ol> : <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">Your assessed skills are at 70% or above. Retake as your skills grow to refresh your roadmap.</p>}
            </div>
          </section>
        </>
      )}

      {!assessment && !status?.has_completed && !result && (
        <section className="rounded-3xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
          <h2 className="font-bold text-slate-900 dark:text-white">How this assessment works</h2>
          <ul className="mt-3 grid gap-3 text-xs text-slate-600 dark:text-slate-300 md:grid-cols-3">
            <li className="flex gap-2"><Target className="h-4 w-4 shrink-0 text-violet-600" /> Questions match your selected career, profile skills, and evidence.</li>
            <li className="flex gap-2"><MessageSquareText className="h-4 w-4 shrink-0 text-violet-600" /> Question types include debugging, code reading, technical choices, and workplace scenarios.</li>
            <li className="flex gap-2"><RotateCcw className="h-4 w-4 shrink-0 text-violet-600" /> Retakes are randomized; previous attempts are preserved and question repeats are avoided when possible.</li>
          </ul>
        </section>
      )}

      {history.length > 0 && !assessment && (
        <section className="rounded-3xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
          <h2 className="font-bold text-slate-900 dark:text-white">Assessment history</h2>
          <div className="mt-3 divide-y divide-slate-100 dark:divide-slate-800">
            {history.map((attempt) => <div key={attempt.attempt_id} className="flex flex-wrap items-center justify-between gap-2 py-3 text-xs"><div><p className="font-semibold text-slate-800 dark:text-slate-200">{attempt.career_title} · {new Date(attempt.submitted_at).toLocaleString()}</p><p className="mt-1 text-slate-500">{attempt.skill_results.length} skills assessed · {attempt.correct_count}/{attempt.total_questions} correct</p></div><span className="rounded-lg bg-violet-50 px-3 py-1.5 font-bold text-violet-700 dark:bg-violet-950 dark:text-violet-300">{attempt.overall_score}%</span></div>)}
          </div>
        </section>
      )}

      {status?.has_completed && !result && !assessment && (
        <div className="flex justify-end"><button onClick={startAssessment} disabled={loading} className="inline-flex items-center gap-2 rounded-xl border border-violet-200 px-4 py-2.5 text-xs font-bold text-violet-700 hover:bg-violet-50 disabled:opacity-50 dark:border-violet-900 dark:text-violet-300 dark:hover:bg-violet-950/40"><RotateCcw className="h-4 w-4" /> Retake assessment</button></div>
      )}
    </div>
  );
};

export default PracticalAssessment;
