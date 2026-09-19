import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  LayoutDashboard, 
  UserCheck, 
  ClipboardCheck, 
  Compass, 
  TrendingUp, 
  ShieldCheck, 
  Map, 
  BarChart3,
  Lock,
  LogOut
} from 'lucide-react';

const Sidebar = () => {
  const { logout } = useAuth();

  const activeClass = "flex items-center space-x-3 px-4 py-3 rounded-xl bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 font-medium transition-all";
  const inactiveClass = "flex items-center space-x-3 px-4 py-3 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 transition-all";

  return (
    <aside className="w-64 border-r border-slate-800 bg-[#0b0f19] p-4 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-4rem)]">
      <div className="space-y-6">
        <div>
          <div className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
            Core Modules
          </div>
          <nav className="space-y-1">
            <NavLink to="/dashboard" className={({ isActive }) => isActive ? activeClass : inactiveClass}>
              <LayoutDashboard className="w-5 h-5" />
              <span>Dashboard</span>
            </NavLink>
            <NavLink to="/profile" className={({ isActive }) => isActive ? activeClass : inactiveClass}>
              <UserCheck className="w-5 h-5" />
              <span>My Profile</span>
            </NavLink>
            <NavLink to="/assessment" className={({ isActive }) => isActive ? activeClass : inactiveClass}>
              <ClipboardCheck className="w-5 h-5" />
              <span>Assessment</span>
            </NavLink>
            <NavLink to="/recommendations" className={({ isActive }) => isActive ? activeClass : inactiveClass}>
              <Compass className="w-5 h-5" />
              <span>Recommendations</span>
            </NavLink>
            <NavLink to="/career/ai-engineer" className={({ isActive }) => isActive ? activeClass : inactiveClass}>
              <TrendingUp className="w-5 h-5" />
              <span>Career Analysis</span>
            </NavLink>
          </nav>
        </div>

        <div>
          <div className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 flex items-center justify-between">
            <span>Enhancement Modules</span>
            <span className="text-[10px] text-emerald-400 font-bold px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">Phase 2</span>
          </div>
          <nav className="space-y-1">
            <NavLink to="/evidence" className={({ isActive }) => isActive ? activeClass : inactiveClass}>
              <ShieldCheck className="w-5 h-5 text-indigo-400" />
              <span>Evidence Engine</span>
            </NavLink>
            <NavLink to="/roadmap" className={({ isActive }) => isActive ? activeClass : inactiveClass}>
              <Map className="w-5 h-5 text-emerald-400" />
              <span>Adaptive Roadmap</span>
            </NavLink>
            <NavLink to="/progress" className={({ isActive }) => isActive ? activeClass : inactiveClass}>
              <BarChart3 className="w-5 h-5 text-cyan-400" />
              <span>Progress Tracker</span>
            </NavLink>
          </nav>
        </div>
      </div>

      <div className="space-y-3">
        <button 
          onClick={logout}
          className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-red-400 hover:bg-red-500/10 border border-red-500/20 font-semibold text-sm transition-all"
        >
          <LogOut className="w-5 h-5" />
          <span>Logout</span>
        </button>

        <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-[11px] text-slate-400">
          <div className="font-semibold text-slate-300">Phase 2 Integration</div>
          <p>Evidence-Based Employability Enhancement live with dynamic recalculations.</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
