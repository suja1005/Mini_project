import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Onboarding from './pages/Onboarding';
import Assessment from './pages/Assessment';
import Recommendations from './pages/Recommendations';
import CareerDetail from './pages/CareerDetail';
import Evidence from './pages/Evidence';
import Roadmap from './pages/Roadmap';
import Progress from './pages/Progress';

import ErrorBoundary from './components/ErrorBoundary';

const RootRedirect = () => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return null;
  return <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <ErrorBoundary>
          <Routes>
            {/* Public Auth Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected Application Routes */}
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><Onboarding /></ProtectedRoute>} />
            <Route path="/onboarding" element={<ProtectedRoute><Onboarding /></ProtectedRoute>} />
            <Route path="/assessment" element={<ProtectedRoute><Assessment /></ProtectedRoute>} />
            <Route path="/recommendations" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
            <Route path="/career" element={<Navigate to="/career/ai-engineer" replace />} />
            <Route path="/career/:careerId" element={<ProtectedRoute><CareerDetail /></ProtectedRoute>} />
            <Route path="/career-analysis" element={<Navigate to="/career/ai-engineer" replace />} />
            <Route path="/career-analysis/:careerId" element={<ProtectedRoute><CareerDetail /></ProtectedRoute>} />
            <Route path="/evidence" element={<ProtectedRoute><Evidence /></ProtectedRoute>} />
            <Route path="/roadmap" element={<ProtectedRoute><Roadmap /></ProtectedRoute>} />
            <Route path="/progress" element={<ProtectedRoute><Progress /></ProtectedRoute>} />

            {/* Root and Catch-all Redirects */}
            <Route path="/" element={<RootRedirect />} />
            <Route path="*" element={<RootRedirect />} />
          </Routes>
        </ErrorBoundary>
      </Router>
    </AuthProvider>
  );
}

export default App;
