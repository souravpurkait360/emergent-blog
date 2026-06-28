import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LayoutDashboard, LogOut, PenSquare, Search, User } from 'lucide-react';
import useAuthStore from '../../store/authStore';

export default function Navbar() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  const handleLogout = async () => { await logout(); navigate('/'); };

  const handleSearch = (event) => {
    event.preventDefault();
    if (searchQuery.trim()) navigate(`/?search=${encodeURIComponent(searchQuery.trim())}`);
  };

  return (
    <nav className="sticky top-0 z-50 bg-surface/80 backdrop-blur-xl border-b border-edge font-body">
      <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between gap-4">
        <Link to="/" className="font-display font-black text-xl tracking-tighter text-ink shrink-0" data-testid="navbar-logo">
          INKFLOW
        </Link>

        <form onSubmit={handleSearch} className="flex-1 max-w-sm hidden md:flex items-center border border-edge bg-wash">
          <Search size={14} className="ml-3 text-ink-muted" />
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search posts..."
            className="w-full bg-transparent px-3 py-2 text-sm focus:outline-none"
            data-testid="navbar-search-input"
          />
        </form>

        <div className="flex items-center gap-3 shrink-0">
          {user ? (
            <>
              <Link to="/write" className="flex items-center gap-1.5 bg-accent text-surface px-4 py-2 text-sm font-medium hover:bg-accent-hover transition-colors" data-testid="write-post-btn">
                <PenSquare size={14} /> Write
              </Link>
              {user.role === 'admin' && (
                <Link to="/admin" title="Admin" data-testid="admin-link" className="text-ink-muted hover:text-ink transition-colors">
                  <LayoutDashboard size={18} />
                </Link>
              )}
              <Link to="/profile" title="Profile" data-testid="profile-link" className="text-ink-muted hover:text-ink transition-colors">
                <User size={18} />
              </Link>
              <button onClick={handleLogout} data-testid="logout-btn" className="text-ink-muted hover:text-ink transition-colors">
                <LogOut size={18} />
              </button>
            </>
          ) : (
            <Link to="/auth" className="bg-ink text-surface px-4 py-2 text-sm hover:bg-ink-muted transition-colors" data-testid="signin-btn">
              Sign In
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
