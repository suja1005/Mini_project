import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import { Link } from 'react-router-dom';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[400px] flex items-center justify-center p-6">
          <div className="glass-card max-w-md w-full p-8 rounded-3xl border border-red-500/20 bg-slate-900/90 text-center space-y-5 shadow-2xl">
            <div className="w-16 h-16 rounded-2xl bg-red-500/10 border border-red-500/30 text-red-400 mx-auto flex items-center justify-center">
              <AlertTriangle className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Something went wrong</h2>
              <p className="text-sm text-slate-400 mt-2">
                An unexpected error occurred while rendering this page.
              </p>
              {this.state.error?.message && (
                <div className="mt-3 p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-left font-mono text-xs text-red-300 break-words">
                  {this.state.error.message}
                </div>
              )}
            </div>
            <div className="flex items-center justify-center space-x-3 pt-2">
              <button
                onClick={() => window.location.reload()}
                className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Reload Page</span>
              </button>
              <Link
                to="/dashboard"
                onClick={() => this.setState({ hasError: false, error: null })}
                className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs flex items-center space-x-2 transition-all"
              >
                <Home className="w-4 h-4" />
                <span>Dashboard</span>
              </Link>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
