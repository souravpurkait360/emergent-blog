import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import PostDetail from './pages/PostDetail';
import PostEditor from './pages/PostEditor';
import Auth from './pages/Auth';
import Profile from './pages/Profile';
import AdminDashboard from './pages/AdminDashboard';
import { Toaster } from 'sonner';
import './App.css';

function ProtectedRoute({ children, admin = false }) {
  const { user } = useAuth();
  if (user === undefined) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-[#002FA7] border-t-transparent rounded-full animate-spin" />
    </div>
  );
  if (!user) return <Navigate to="/auth" replace />;
  if (admin && user.role !== 'admin') return <Navigate to="/" replace />;
  return children;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-[#FDFDFD]">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/post/:slug" element={<PostDetail />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/write" element={<ProtectedRoute><PostEditor /></ProtectedRoute>} />
            <Route path="/write/:slug" element={<ProtectedRoute><PostEditor /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
            <Route path="/admin" element={<ProtectedRoute admin><AdminDashboard /></ProtectedRoute>} />
          </Routes>
        </div>
        <Toaster position="bottom-right" richColors />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
