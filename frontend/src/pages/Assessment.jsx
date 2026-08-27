import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentService } from '../services/assessmentService';
import { recommendationService } from '../services/recommendationService';
import PhaseBanner from '../components/PhaseBanner';
import { ClipboardCheck, CheckCircle2, ArrowRight, Brain, Calculator, Code2, Loader2 } from 'lucide-react';

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
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Loading 15 Assessment Questions...</span>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-3">
            <ClipboardCheck className="w-7 h-7 text-indigo-400" />
            <span>Skill & Aptitude Assessment</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Evaluates Logical Reasoning, Numerical Ability, and Technical Aptitude (15 questions).
          </p>
        </div>
        <div className="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold border border-indigo-500/20">
          Module C Connected
        </div>
      </div>

      <PhaseBanner 
        title="Module C — Assessment Result Processing"
        message="Submitting calculates objective scores across Logical Reasoning, Numerical Ability, and Technical Aptitude, updating student profile metrics in MongoDB."
      />

      {/* Category Overview */}
      <div className="grid grid-cols-3 gap-4">
        <div className="glass-card p-4 rounded-2xl border border-slate-800 flex items-center space-x-3">
          <Brain className="w-6 h-6 text-indigo-400" />
          <div>
            <div className="text-xs font-semibold text-slate-400">Logical Reasoning</div>
            <div className="text-sm font-bold text-white">5 Questions</div>
          </div>
        </div>
        <div className="glass-card p-4 rounded-2xl border border-slate-800 flex items-center space-x-3">
          <Calculator className="w-6 h-6 text-emerald-400" />
          <div>
            <div className="text-xs font-semibold text-slate-400">Numerical Ability</div>
            <div className="text-sm font-bold text-white">5 Questions</div>
          </div>
        </div>
        <div className="glass-card p-4 rounded-2xl border border-slate-800 flex items-center space-x-3">
          <Code2 className="w-6 h-6 text-amber-400" />
          <div>
            <div className="text-xs font-semibold text-slate-400">Technical Aptitude</div>
            <div className="text-sm font-bold text-white">5 Questions</div>
          </div>
        </div>
      </div>

      {/* Completed Result Banner */}
      {result && result.is_completed && (
        <div className="glass-card p-6 rounded-3xl border border-emerald-500/30 bg-emerald-950/20 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <CheckCircle2 className="w-6 h-6 text-emerald-400" />
              <div>
                <h3 className="text-base font-bold text-white">Assessment Completed ✓</h3>
                <p className="text-xs text-emerald-300/80">Result saved to MongoDB database for current student session.</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-extrabold text-emerald-400">{result.overall_score}%</div>
              <div className="text-[10px] text-slate-400 uppercase font-semibold">Overall Score</div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3 text-center pt-2">
            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="text-xs text-slate-400">Logical Reasoning</div>
              <div className="text-sm font-bold text-indigo-300 mt-1">{result.logical_score}%</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="text-xs text-slate-400">Numerical Ability</div>
              <div className="text-sm font-bold text-emerald-300 mt-1">{result.numerical_score}%</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="text-xs text-slate-400">Technical Aptitude</div>
              <div className="text-sm font-bold text-amber-300 mt-1">{result.technical_score}%</div>
            </div>
          </div>
        </div>
      )}

      {/* Questions Form */}
      <div className="glass-card p-6 md:p-8 rounded-3xl border border-slate-800 space-y-6">
        <h2 className="text-lg font-bold text-white">15 Assessment Questions</h2>

        {questions.map((q, idx) => (
          <div key={q.id} className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                {q.category}
              </span>
              <span className="text-xs text-slate-500">Question {idx + 1} of {questions.length}</span>
            </div>

            <p className="text-sm font-semibold text-slate-200">{q.question}</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {q.options.map((opt, optIdx) => {
                const isSelected = answers[String(q.id)] === optIdx;
                return (
                  <div 
                    key={optIdx} 
                    onClick={() => handleSelectOption(q.id, optIdx)}
                    className={`p-3 rounded-xl border text-xs font-medium cursor-pointer transition-all ${
                      isSelected 
                        ? "bg-indigo-600/30 border-indigo-500 text-indigo-200 flex items-center justify-between shadow-md shadow-indigo-600/20"
                        : "bg-slate-800/40 border-slate-700/60 text-slate-300 hover:bg-slate-800"
                    }`}
                  >
                    <span>{opt}</span>
                    {isSelected && <CheckCircle2 className="w-4 h-4 text-indigo-400" />}
                  </div>
                );
              })}
            </div>
          </div>
        ))}

        <div className="flex justify-between items-center pt-4 border-t border-slate-800">
          <button 
            onClick={handleSubmitAssessment}
            disabled={submitting}
            className="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/30 flex items-center space-x-2 disabled:opacity-50"
          >
            {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <ClipboardCheck className="w-4 h-4" />}
            <span>Submit Assessment Answers</span>
          </button>

          <button 
            onClick={handleAnalyzeCareer}
            className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm shadow-lg shadow-emerald-600/30 flex items-center space-x-2"
          >
            <span>Analyze My Career</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Assessment;
