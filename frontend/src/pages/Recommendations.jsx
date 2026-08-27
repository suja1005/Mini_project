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
      <div className="h-64 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm">Calculating Multi-Career Recommendations via Explainable Scoring Model...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-3">
            <Compass className="w-7 h-7 text-indigo-400" />
            <span>Multi-Career Recommendations</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Top 3–5 matched career paths evaluated via explainable weighted scoring (Technical 40%, Interest 20%, Aptitude 15%, Academic 10%, Preference 15%).
          </p>
        </div>
        <div className="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold border border-indigo-500/20">
          Module D Connected
        </div>
      </div>

      <PhaseBanner 
        title="Module D — Explainable Recommendation Scoring"
        message="The algorithm calculates exact matching scores deterministically across 20 structured career profiles based on your authenticated student session."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {recommendations.map((career) => (
          <div key={career.id} className="glass-card p-6 rounded-3xl border border-slate-800 glass-card-hover flex flex-col justify-between space-y-5">
            <div>
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                    {career.category}
                  </span>
                  <h3 className="text-xl font-bold text-white mt-2 flex items-center space-x-2">
                    <span>{career.title}</span>
                    {career.fit_score >= 85 && <Sparkles className="w-4 h-4 text-amber-400" />}
                  </h3>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-extrabold text-emerald-400">{career.fit_score}%</div>
                  <div className="text-[10px] text-slate-400 uppercase font-semibold">Career Fit</div>
                </div>
              </div>

              <p className="text-xs text-slate-400 mt-2 line-clamp-2">{career.description}</p>

              <div className="space-y-3 mt-4">
                <div>
                  <div className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                    Why Recommended
                  </div>
                  <ul className="space-y-1">
                    {career.why_recommended?.map((item, idx) => (
                      <li key={idx} className="text-xs text-slate-300 flex items-center space-x-2">
                        <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <div className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                    Needs Improvement
                  </div>
                  <ul className="space-y-1">
                    {career.needs_improvement?.map((item, idx) => (
                      <li key={idx} className="text-xs text-amber-300/90 flex items-center space-x-2">
                        <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800/80">
              <Link 
                to={`/career/${career.id}`}
                className="w-full py-2.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 font-semibold text-xs border border-indigo-500/30 flex items-center justify-center space-x-2 transition-all"
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
