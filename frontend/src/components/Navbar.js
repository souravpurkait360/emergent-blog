import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { PenSquare, LogOut, User, LayoutDashboard, Search } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [search, setSearch] = useState('');

  const handleLogout = () => { logout(); navigate('/'); };
  const handleSearch = (e) => {
    e.preventDefault();
    if (search.trim()) navigate(`/?search=${encodeURIComponent(search.trim())}`);
  };

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-zinc-100" style={{fontFamily: "'IBM Plex Sans', sans-serif"}}>
      <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between gap-4">
        <Link to="/" className="font-black text-xl tracking-tighter text-[#050505] shrink-0" style={{fontFamily:"'Outfit',sans-serif"}} data-testid="navbar-logo">
          INKFLOW
        </Link>

        <form onSubmit={handleSearch} className="flex-1 max-w-sm hidden md:flex items-center border border-[#E4E4E7] bg-[#F4F4F5]">
          <Search size={14} className="ml-3 text-[#52525B]" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search posts..."
            className="w-full bg-transparent px-3 py-2 text-sm focus:outline-none"
            data-testid="navbar-search-input"
          />
        </form>

        <div className="flex items-center gap-3 shrink-0">
          {user ? (
            <>
              <Link
                to="/write"
                className="flex items-center gap-1.5 bg-[#002FA7] text-white px-4 py-2 text-sm font-medium hover:bg-[#002280] transition-colors"
                data-testid="write-post-btn"
              >
                <PenSquare size={14} />
                Write
              </Link>
              {user.role === 'admin' && (
                <Link to="/admin" title="Admin" data-testid="admin-link" className="text-[#52525B] hover:text-[#050505]">
                  <LayoutDashboard size={18} />
                </Link>
              )}
              <Link to="/profile" title="Profile" data-testid="profile-link" className="text-[#52525B] hover:text-[#050505]">
                <User size={18} />
              </Link>
              <button onClick={handleLogout} data-testid="logout-btn" className="text-[#52525B] hover:text-[#050505]">
                <LogOut size={18} />
              </button>
            </>
          ) : (
            <Link
              to="/auth"
              className="bg-[#050505] text-white px-4 py-2 text-sm hover:bg-zinc-800 transition-colors"
              data-testid="signin-btn"
            >
              Sign In
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
