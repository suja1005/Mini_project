import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import logo from '../assets/career-guidance-logo.png';
import { 
  LayoutDashboard, 
  UserCheck, 
  ClipboardCheck, 
  Compass, 
  TrendingUp, 
  ShieldCheck, 
  Map, 
  BarChart3,
  Settings,
  HelpCircle,
  LogOut,
  PanelLeftClose,
  PanelLeft
} from 'lucide-react';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, badge: null },
    { to: '/profile', label: 'My Profile', icon: UserCheck, badge: null },
    { to: '/assessment', label: 'Assessment', icon: ClipboardCheck, badge: null },
    { to: '/recommendations', label: 'Recommendations', icon: Compass, badge: null },
    { to: '/career/ai-engineer', label: 'Career Analysis', icon: TrendingUp, matchPrefix: '/career' },
  ];

  const phase2Items = [
    { to: '/evidence', label: 'Evidence Engine', icon: ShieldCheck, badge: 'NEW', badgeColor: 'bg-indigo-600 text-white' },
    { to: '/practical-assessment', label: 'Practical Assessment', icon: ClipboardCheck, badge: null },
    { to: '/roadmap', label: 'Adaptive Roadmap', icon: Map, badge: null },
    { to: '/progress', label: 'Progress Tracker', icon: BarChart3, badge: null },
  ];

  const activeLinkClass = 
    "flex items-center justify-between px-3.5 py-2.5 rounded-xl bg-indigo-50/90 text-indigo-700 font-semibold text-sm transition-all border border-indigo-100/80 dark:bg-indigo-950/40 dark:text-indigo-300 dark:border-indigo-500/20 shadow-xs";
  const inactiveLinkClass = 
    "flex items-center justify-between px-3.5 py-2.5 rounded-xl text-slate-600 hover:text-white hover:bg-indigo-600 font-medium text-sm transition-all dark:text-slate-400 dark:hover:text-white dark:hover:bg-indigo-600";

  return (
    <>
      <aside className="w-68 shrink-0 bg-white dark:bg-[#0d1322] border-r border-gray-200/80 dark:border-slate-800/80 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-4rem)] p-4 select-none">
        <div className="space-y-5">
          {/* Brand header */}
          <div className="flex items-center justify-between px-2 pt-1">
            <NavLink to="/dashboard" className="flex items-center space-x-2.5 group">
              <img src={logo} alt="AI Career Guidance" className="w-8 h-6 object-contain shrink-0 transition-transform group-hover:scale-105" />
              <span className="font-semibold text-sm tracking-tight text-slate-900 dark:text-white">
                Career Guidance
              </span>
            </NavLink>
            <button 
              type="button"
              title="Sidebar View"
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <PanelLeft className="w-4 h-4" />
            </button>
          </div>

          {/* Main Navigation Menu */}
          <div className="space-y-1">
            <nav className="space-y-0.5">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = item.matchPrefix 
                  ? location.pathname.startsWith(item.matchPrefix)
                  : location.pathname === item.to;

                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={isActive ? activeLinkClass : inactiveLinkClass}
                  >
                    <div className="flex items-center space-x-3">
                      <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400 dark:text-slate-500'}`} />
                      <span>{item.label}</span>
                    </div>
                    {item.badge && (
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${item.badgeColor || 'bg-indigo-100 text-indigo-700'}`}>
                        {item.badge}
                      </span>
                    )}
                  </NavLink>
                );
              })}
            </nav>
          </div>

          {/* Phase 2 Enhancement Section */}
          <div className="pt-2">
            <div className="px-3 text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2 flex items-center justify-between">
              <span>Enhancement</span>
              <span className="text-[10px] font-semibold px-1.5 py-0.2 rounded bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 border border-emerald-200/60 dark:border-emerald-800/40">
                Phase 2
              </span>
            </div>
            <nav className="space-y-0.5">
              {phase2Items.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.to;

                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={isActive ? activeLinkClass : inactiveLinkClass}
                  >
                    <div className="flex items-center space-x-3">
                      <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400 dark:text-slate-500'}`} />
                      <span>{item.label}</span>
                    </div>
                    {item.badge && (
                      <span className={`text-[9px] font-extrabold px-1.5 py-0.5 rounded-full ${item.badgeColor || 'bg-indigo-600 text-white'}`}>
                        {item.badge}
                      </span>
                    )}
                  </NavLink>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Bottom Section: User Info */}
        <div className="pt-4 border-t border-gray-100 dark:border-slate-800 space-y-3">
          {/* User profile row */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-gray-200/60 dark:border-slate-700/60">
            <div className="flex items-center space-x-2.5 min-w-0">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-xs shrink-0 shadow-xs">
                {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'S'}
              </div>
              <div className="min-w-0 text-left">
                <div className="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate">
                  {user?.full_name || 'Emilia Caitlin'}
                </div>
                <div className="text-[11px] text-slate-400 dark:text-slate-500 truncate">
                  {user?.email || 'student@career.ai'}
                </div>
              </div>
            </div>

            <button
              type="button"
              onClick={logout}
              title="Sign Out"
              className="p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-lg transition-colors shrink-0"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

    </>
  );
};

export default Sidebar;
