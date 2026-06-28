import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { useEffect } from 'react';
import { Toaster } from 'sonner';
import './App.css';
import Navbar from './components/common/Navbar';
import LoadingSpinner from './components/common/LoadingSpinner';
import Home from './pages/Home';
import PostDetail from './pages/PostDetail';
import PostEditor from './pages/PostEditor';
import Auth from './pages/Auth';
import Profile from './pages/Profile';
import AdminDashboard from './pages/AdminDashboard';
import useAuthStore from './store/authStore';

function ProtectedRoute({ children, adminOnly = false }) {
  const user = useAuthStore((state) => state.user);
  if (user === undefined) return <LoadingSpinner />;
  if (!user) return <Navigate to="/auth" replace />;
  if (adminOnly && user.role !== 'admin') return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  const init = useAuthStore((state) => state.init);

  useEffect(() => { init(); }, [init]);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-canvas font-body">
        <Navbar />
        <Routes>
          <Route path="/"              element={<Home />} />
          <Route path="/post/:slug"    element={<PostDetail />} />
          <Route path="/auth"          element={<Auth />} />
          <Route path="/write"         element={<ProtectedRoute><PostEditor /></ProtectedRoute>} />
          <Route path="/write/:slug"   element={<ProtectedRoute><PostEditor /></ProtectedRoute>} />
          <Route path="/profile"       element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/admin"         element={<ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>} />
        </Routes>
      </div>
      <Toaster position="bottom-right" richColors />
    </BrowserRouter>
  );
}
