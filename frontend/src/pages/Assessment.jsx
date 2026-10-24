import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentService } from '../services/assessmentService';
import { recommendationService } from '../services/recommendationService';
import PhaseBanner from '../components/PhaseBanner';
import { ClipboardCheck, CheckCircle2, ArrowRight, Brain, Calculator, Code2, Loader2, Sparkles } from 'lucide-react';

const Assessment = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => {
    const initAssessment = async () => {
      setLoading(true);
      try {
        const [qData, resData] = await Promise.allSettled([
          assessmentService.getQuestions(),
          assessmentService.getResults()
        ]);

        if (qData.status === 'fulfilled') setQuestions(qData.value);
        if (resData.status === 'fulfilled') setResult(resData.value);
      } catch (err) {
        console.error("Error fetching assessment:", err);
      } finally {
        setLoading(false);
      }
    };

    initAssessment();
  }, []);

  const handleSelectOption = (questionId, optionIdx) => {
    setAnswers(prev => ({
      ...prev,
      [String(questionId)]: optionIdx
    }));
  };

  const handleSubmitAssessment = async () => {
    setSubmitting(true);
    try {
      const res = await assessmentService.submitAssessment(answers);
      setResult(res);
    } catch (err) {
      console.error("Error submitting assessment:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleAnalyzeCareer = async () => {
    try {
      await recommendationService.generateRecommendations();
    } catch (err) {
      console.error("Error generating recommendations:", err);
    }
    navigate('/recommendations');
  };

  if (loading) {
    return (
      <div className="h-96 flex flex-col items-center justify-center space-y-3 text-slate-500">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
        <span className="text-sm font-medium">Loading Assessment Questions...</span>
      </div>
    );
  }

  const answeredCount = Object.keys(answers).length;
  const progressPercent = questions.length > 0 ? Math.round((answeredCount / questions.length) * 100) : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in pb-12">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white flex items-center space-x-3 tracking-tight">
            <div className="p-2 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400">
              <ClipboardCheck className="w-6 h-6" />
            </div>
            <span>Skill & Aptitude Assessment</span>
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Evaluates Logical Reasoning, Numerical Ability, and Technical Aptitude ({questions.length} questions).
          </p>
        </div>
        <div className="px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-400 text-xs font-semibold border border-indigo-200/80 dark:border-indigo-800/40 w-fit">
          Module C Connected
        </div>
      </div>

      <PhaseBanner 
        title="Module C — Assessment Result Processing"
        message="Submitting calculates objective scores across Logical Reasoning, Numerical Ability, and Technical Aptitude, updating student profile metrics in MongoDB."
      />

      {/* Category Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white dark:bg-[#111827] p-4 rounded-2xl border border-gray-200/80 dark:border-slate-800 shadow-xs flex items-center space-x-3.5">
          <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 border border-indigo-100 dark:border-indigo-800/40">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs font-semibold text-slate-500 dark:text-slate-400">Logical Reasoning</div>
            <div className="text-sm font-bold text-slate-900 dark:text-white">5 Questions</div>
          </div>
        </div>

        <div className="bg-white dark:bg-[#111827] p-4 rounded-2xl border border-gray-200/80 dark:border-slate-800 shadow-xs flex items-center space-x-3.5">
          <div className="p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-800/40">
            <Calculator className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs font-semibold text-slate-500 dark:text-slate-400">Numerical Ability</div>
            <div className="text-sm font-bold text-slate-900 dark:text-white">5 Questions</div>
          </div>
        </div>

        <div className="bg-white dark:bg-[#111827] p-4 rounded-2xl border border-gray-200/80 dark:border-slate-800 shadow-xs flex items-center space-x-3.5">
          <div className="p-2.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 border border-amber-100 dark:border-amber-800/40">
            <Code2 className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs font-semibold text-slate-500 dark:text-slate-400">Technical Aptitude</div>
            <div className="text-sm font-bold text-slate-900 dark:text-white">5 Questions</div>
          </div>
        </div>
      </div>

      {/* Completed Result Banner */}
      {result && result.is_completed && (
        <div className="bg-white dark:bg-[#111827] p-6 rounded-3xl border border-emerald-300 dark:border-emerald-800/60 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 flex items-center justify-center font-bold">
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">Assessment Completed</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">Results saved and applied to your career readiness scoring.</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400">{result.overall_score}%</div>
              <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Overall Score</div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3 text-center pt-2">
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-gray-200/60 dark:border-slate-700">
              <div className="text-xs text-slate-500 dark:text-slate-400">Logical Reasoning</div>
              <div className="text-sm font-bold text-indigo-600 dark:text-indigo-300 mt-1">{result.logical_score}%</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-gray-200/60 dark:border-slate-700">
              <div className="text-xs text-slate-500 dark:text-slate-400">Numerical Ability</div>
              <div className="text-sm font-bold text-emerald-600 dark:text-emerald-300 mt-1">{result.numerical_score}%</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-gray-200/60 dark:border-slate-700">
              <div className="text-xs text-slate-500 dark:text-slate-400">Technical Aptitude</div>
              <div className="text-sm font-bold text-amber-600 dark:text-amber-300 mt-1">{result.technical_score}%</div>
            </div>
          </div>
        </div>
      )}

      {/* Questions Form */}
      <div className="bg-white dark:bg-[#111827] p-6 md:p-8 rounded-3xl border border-gray-200/80 dark:border-slate-800 shadow-xs space-y-6">
        <div className="flex items-center justify-between pb-3 border-b border-gray-100 dark:border-slate-800">
          <div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white">
              Questions Checklist ({answeredCount}/{questions.length} answered)
            </h2>
            <div className="w-48 bg-gray-200 dark:bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div 
                className="bg-indigo-600 h-full rounded-full transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
          <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400">
            {progressPercent}% Complete
          </span>
        </div>

        <div className="space-y-4">
          {questions.map((q, idx) => (
            <div key={q.id} className="p-5 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200/60 dark:border-slate-700/60 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-400 border border-indigo-200/60 dark:border-indigo-800/40">
                  {q.category}
                </span>
                <span className="text-xs font-medium text-slate-400">Question {idx + 1} of {questions.length}</span>
              </div>

              <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">{q.question}</p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
                {q.options.map((opt, optIdx) => {
                  const isSelected = answers[String(q.id)] === optIdx;
                  return (
                    <div 
                      key={optIdx} 
                      onClick={() => handleSelectOption(q.id, optIdx)}
                      className={`p-3 rounded-xl border text-xs font-medium cursor-pointer transition-all flex items-center justify-between ${
                        isSelected 
                          ? "bg-indigo-50 dark:bg-indigo-950/60 border-indigo-600 dark:border-indigo-500 text-indigo-700 dark:text-indigo-200 shadow-xs ring-1 ring-indigo-500"
                          : "bg-white dark:bg-slate-800 border-gray-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:border-gray-300 dark:hover:border-slate-600 hover:bg-gray-50/50"
                      }`}
                    >
                      <span>{opt}</span>
                      {isSelected && <CheckCircle2 className="w-4 h-4 text-indigo-600 dark:text-indigo-400 shrink-0 ml-2" />}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row justify-between items-center gap-3 pt-4 border-t border-gray-100 dark:border-slate-800">
          <button 
            type="button"
            onClick={handleSubmitAssessment}
            disabled={submitting}
            className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold text-xs shadow-xs flex items-center justify-center space-x-2 disabled:opacity-50 transition-all active:scale-95"
          >
            {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <ClipboardCheck className="w-4 h-4" />}
            <span>Submit Assessment Answers</span>
          </button>

          <button 
            type="button"
            onClick={handleAnalyzeCareer}
            className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-xs flex items-center justify-center space-x-2 transition-all active:scale-95"
          >
            <span>Analyze My Career Recommendations</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Assessment;
