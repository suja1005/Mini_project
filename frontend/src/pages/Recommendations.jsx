import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { recommendationService } from '../services/recommendationService';
import PhaseBanner from '../components/PhaseBanner';
import { Compass, Check, AlertTriangle, ArrowRight, Loader2, Sparkles } from 'lucide-react';

const Recommendations = () => {
  const [loading, setLoading] = useState(true);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const fetchRecs = async () => {
      setLoading(true);
      try {
        const data = await recommendationService.getRecommendations();
        if (data && data.top_recommendations) {
          setRecommendations(data.top_recommendations);
        }
      } catch (err) {
        console.error("Error fetching recommendations:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecs();
  }, []);

  if (loading) {
    return (
      <div className="h-96 flex flex-col items-center justify-center space-y-3 text-slate-500">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
        <span className="text-sm font-medium">Calculating Explainable Recommendations...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto animate-fade-in pb-12">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white flex items-center space-x-3 tracking-tight">
            <div className="p-2 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400">
              <Compass className="w-6 h-6" />
            </div>
            <span>Career Recommendations</span>
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Top matched career paths evaluated via explainable weighted scoring (Technical 40%, Interest 20%, Aptitude 15%, Academic 10%, Preference 15%).
          </p>
        </div>
        <div className="px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-400 text-xs font-semibold border border-indigo-200/80 dark:border-indigo-800/40 w-fit">
          Explainable Model
        </div>
      </div>

      <PhaseBanner 
        title="Module D — Explainable Recommendation Scoring"
        message="The algorithm calculates exact matching scores deterministically across 20 structured career profiles based on your authenticated student session."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {recommendations.map((career) => (
          <div 
            key={career.id} 
            className="bg-white dark:bg-[#111827] p-6 rounded-3xl border border-gray-200/80 dark:border-slate-800 shadow-xs hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-5 group"
          >
            <div>
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-gray-200/60 dark:border-slate-700">
                    {career.category}
                  </span>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-2 flex items-center space-x-2">
                    <span>{career.title}</span>
                    {career.fit_score >= 85 && <Sparkles className="w-4 h-4 text-amber-500" />}
                  </h3>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400">{career.fit_score}%</div>
                  <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Career Fit</div>
                </div>
              </div>

              <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 line-clamp-2 leading-relaxed">{career.description}</p>

              <div className="space-y-3 mt-4">
                <div className="p-3 rounded-2xl bg-slate-50 dark:bg-[#162035] border border-gray-200/60 dark:border-slate-700/60">
                  <div className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-2">
                    Why Recommended
                  </div>
                  <ul className="space-y-1.5">
                    {career.why_recommended?.map((item, idx) => (
                      <li key={idx} className="text-xs text-slate-600 dark:text-slate-300 flex items-start space-x-2">
                        <Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {career.needs_improvement?.length > 0 && (
                  <div className="p-3 rounded-2xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-800/40">
                    <div className="text-xs font-bold text-amber-800 dark:text-amber-300 uppercase tracking-wider mb-2">
                      Needs Improvement
                    </div>
                    <ul className="space-y-1.5">
                      {career.needs_improvement?.map((item, idx) => (
                        <li key={idx} className="text-xs text-amber-900 dark:text-amber-200 flex items-start space-x-2">
                          <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            <div className="pt-3 border-t border-gray-100 dark:border-slate-800">
              <Link 
                to={`/career/${career.id}`}
                className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-semibold text-xs flex items-center justify-center space-x-2 shadow-xs transition-all"
              >
                <span>View Career Decision & Risk Analysis</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;
