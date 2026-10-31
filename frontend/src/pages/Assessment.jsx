import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentService } from '../services/assessmentService';
import { recommendationService } from '../services/recommendationService';
import PhaseBanner from '../components/PhaseBanner';
import { 
  ClipboardCheck, 
  CheckCircle2, 
  ArrowRight, 
  Brain, 
  Calculator, 
  Code2, 
  Loader2, 
  Sparkles,
  AlertTriangle,
  RotateCcw,
  Check,
  X
} from 'lucide-react';

const Assessment = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const initAssessment = async () => {
    setLoading(true);
    setError(null);
    try {
      const [qData, resData] = await Promise.allSettled([
        assessmentService.getQuestions(),
        assessmentService.getResults()
      ]);

      if (qData.status === 'fulfilled') setQuestions(qData.value);
      if (resData.status === 'fulfilled') setResult(resData.value);
    } catch (err) {
      console.error("Error fetching assessment:", err);
      setError("Failed to load questions. Please check your network connection.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    initAssessment();
  }, []);

  const handleSelectOption = (questionId, optionVal) => {
    setAnswers(prev => ({
      ...prev,
      [String(questionId)]: optionVal
    }));
  };

  const handleSubmitAssessment = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const res = await assessmentService.submitAssessment(answers);
      setResult(res);
    } catch (err) {
      console.error("Error submitting assessment:", err);
      setError(err.response?.data?.detail || "Error submitting assessment answers.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetakeAssessment = async () => {
    setAnswers({});
    setResult(null);
    await initAssessment();
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
        <span className="text-sm font-medium">Loading Personalized Assessment Questions...</span>
      </div>
    );
  }

  const answeredCount = Object.keys(answers).length;
  const progressPercent = questions.length > 0 ? Math.round((answeredCount / questions.length) * 100) : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white flex items-center space-x-3 tracking-tight">
            <div className="p-2 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400">
              <ClipboardCheck className="w-6 h-6" />
            </div>
            <span>Dynamic Personalized Skill Assessment</span>
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Questions dynamically matched to your profile interests, career target, and skills ({questions.length} questions).
          </p>
        </div>
        <div className="px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 text-xs font-semibold border border-emerald-200 dark:border-emerald-800 w-fit">
          AI Personalized Selection Active
        </div>
      </div>

      <PhaseBanner 
        title="Dynamic Personalized Assessment Engine"
        message="Questions are selected randomly from the question bank matching your domain interests and skill level, excluding previously attempted questions. Final score and skill analytics are calculated strictly on the backend."
      />

      {error && (
        <div className="p-4 rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 text-xs flex items-center space-x-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Completed Result Banner */}
      {result && result.is_completed && (
        <div className="bg-white dark:bg-[#111827] p-6 rounded-3xl border border-emerald-300 dark:border-emerald-800/60 shadow-sm space-y-5 animate-in fade-in">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center space-x-3.5">
              <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 flex items-center justify-center font-bold shadow-xs">
                <CheckCircle2 className="w-7 h-7" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Assessment Submitted & Scored</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  {result.correct_count} of {result.total_questions} questions correct • Model-verified score
                </p>
              </div>
            </div>
            <div className="text-right flex items-center space-x-4">
              <div>
                <div className="text-3xl font-black text-emerald-600 dark:text-emerald-400">{result.overall_score}%</div>
                <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Overall Score</div>
              </div>
              <button
                onClick={handleRetakeAssessment}
                className="px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors flex items-center space-x-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Take Another Assessment</span>
              </button>
            </div>
          </div>

          {/* Categorical Scores */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-center">
            <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700">
              <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">Logical Reasoning</div>
              <div className="text-lg font-bold text-indigo-600 dark:text-indigo-300 mt-0.5">{result.logical_score}%</div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700">
              <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">Numerical Ability</div>
              <div className="text-lg font-bold text-emerald-600 dark:text-emerald-300 mt-0.5">{result.numerical_score}%</div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700">
              <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">Technical Domain</div>
              <div className="text-lg font-bold text-amber-600 dark:text-amber-300 mt-0.5">{result.technical_score}%</div>
            </div>
          </div>

          {/* Weak Topics */}
          {result.weak_topics?.length > 0 && (
            <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/60 space-y-1.5 text-xs">
              <span className="font-bold text-amber-800 dark:text-amber-300 uppercase tracking-wider flex items-center space-x-1.5">
                <AlertTriangle className="w-4 h-4" />
                <span>Areas for Improvement</span>
              </span>
              <p className="text-slate-600 dark:text-slate-400">
                Focus on reviewing: {result.weak_topics.join(', ')}
              </p>
            </div>
          )}

          {/* Itemized Question Reviews with Explanations */}
          {result.reviews && result.reviews.length > 0 && (
            <div className="space-y-3 pt-3 border-t border-slate-100 dark:border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Detailed Answers & Pedagogical Explanations
              </h4>
              <div className="space-y-2.5 max-h-96 overflow-y-auto pr-1">
                {result.reviews.map((rev, idx) => (
                  <div
                    key={idx}
                    className={`p-3.5 rounded-xl border text-xs space-y-1.5 ${
                      rev.is_correct
                        ? 'bg-emerald-50/40 dark:bg-emerald-950/10 border-emerald-200 dark:border-emerald-800/40'
                        : 'bg-red-50/40 dark:bg-red-950/10 border-red-200 dark:border-red-800/40'
                    }`}
                  >
                    <div className="flex items-center justify-between font-bold">
                      <span className="text-slate-800 dark:text-slate-200">
                        Q{idx + 1}: {rev.question}
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
                    {rev.explanation && (
                      <div className="text-[11px] text-slate-500 dark:text-slate-400 pt-1 border-t border-slate-200/40 dark:border-slate-800">
                        <strong>Explanation:</strong> {rev.explanation}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Questions Form */}
      <div className="bg-white dark:bg-[#111827] p-6 md:p-8 rounded-3xl border border-gray-200/80 dark:border-slate-800 shadow-sm space-y-6">
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
            <div key={q.id || q.question_id || idx} className="p-5 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200/60 dark:border-slate-700/60 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-400 border border-indigo-200/60 dark:border-indigo-800/40">
                  {q.skill || q.category || "Technical"} • {q.topic || "General"}
                </span>
                <span className="text-xs font-medium text-slate-400">Question {idx + 1} of {questions.length}</span>
              </div>

              <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">{q.question}</p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
                {q.options?.map((opt, optIdx) => {
                  const qKey = String(q.id || q.question_id);
                  const isSelected = answers[qKey] === opt;
                  return (
                    <div 
                      key={optIdx} 
                      onClick={() => handleSelectOption(qKey, opt)}
                      className={`p-3 rounded-xl border text-xs font-medium cursor-pointer transition-all flex items-center justify-between ${
                        isSelected 
                          ? "bg-indigo-50 dark:bg-indigo-950/60 border-indigo-600 dark:border-indigo-500 text-indigo-700 dark:text-indigo-200 shadow-xs ring-1 ring-indigo-500 font-bold"
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
            disabled={submitting || answeredCount < questions.length}
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
