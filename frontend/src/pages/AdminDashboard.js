import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Trash2, Plus, Users, FileText, Tag, Layers } from 'lucide-react';
import { toast } from 'sonner';
import client from '../api/client';

function Tab({ active, onClick, children, icon: Icon }) {
  return (
    <button onClick={onClick}
      className={`flex items-center gap-2 px-5 py-3 text-sm font-medium border-b-2 transition-colors ${active ? 'border-[#002FA7] text-[#002FA7]' : 'border-transparent text-[#52525B] hover:text-[#050505]'}`}>
      <Icon size={16} /> {children}
    </button>
  );
}

export default function AdminDashboard() {
  const [tab, setTab] = useState('posts');
  const [posts, setPosts] = useState([]);
  const [users, setUsers] = useState([]);
  const [categories, setCategories] = useState([]);
  const [newCat, setNewCat] = useState('');
  const [stats, setStats] = useState({ posts: 0, users: 0, categories: 0 });

  useEffect(() => {
    // Load stats on mount
    Promise.all([
      client.get('/posts/admin/').then(r => { const d = r.data; return d.count || (d.results || d).length; }),
      client.get('/auth/users/').then(r => { const d = r.data; return d.count || (d.results || d).length; }),
      client.get('/categories/').then(r => { const d = r.data; return d.count || (d.results || d).length; }),
    ]).then(([p, u, c]) => setStats({ posts: p, users: u, categories: c })).catch(() => {});
  }, []);

  useEffect(() => {
    if (tab === 'posts') client.get('/posts/admin/').then(r => setPosts(r.data.results || r.data || []));
    if (tab === 'users') client.get('/auth/users/').then(r => setUsers(r.data.results || r.data || []));
    if (tab === 'categories') client.get('/categories/').then(r => setCategories(r.data.results || r.data || []));
  }, [tab]);

  const deletePost = async (id) => {
    if (!window.confirm('Delete this post?')) return;
    try {
      await client.delete(`/posts/admin/${id}/`);
      setPosts(prev => prev.filter(p => p.id !== id));
      toast.success('Post deleted');
    } catch { toast.error('Delete failed'); }
  };

  const updateRole = async (userId, role) => {
    try {
      const { data } = await client.patch(`/auth/users/${userId}/role/`, { role });
      setUsers(prev => prev.map(u => u.id === userId ? data : u));
      toast.success('Role updated');
    } catch { toast.error('Update failed'); }
  };

  const addCategory = async (e) => {
    e.preventDefault();
    if (!newCat.trim()) return;
    try {
      const { data } = await client.post('/categories/', { name: newCat });
      setCategories(prev => [...prev, data]);
      setNewCat('');
      toast.success('Category added');
    } catch { toast.error('Failed to add category'); }
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-12" data-testid="admin-dashboard">
      <h1 className="text-3xl font-black tracking-tight text-[#050505] mb-8" style={{fontFamily:"'Outfit',sans-serif"}}>Admin Dashboard</h1>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Total Posts', val: stats.posts, icon: FileText },
          { label: 'Users', val: stats.users, icon: Users },
          { label: 'Categories', val: stats.categories, icon: Layers },
        ].map(({ label, val, icon: Icon }) => (
          <div key={label} className="border border-[#E4E4E7] bg-white p-6">
            <Icon size={20} className="text-[#002FA7] mb-2" />
            <p className="text-2xl font-black text-[#050505]" style={{fontFamily:"'Outfit',sans-serif"}}>{val}</p>
            <p className="text-xs uppercase tracking-wider text-[#52525B] mt-1">{label}</p>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="border-b border-[#E4E4E7] flex mb-6">
        <Tab active={tab === 'posts'} onClick={() => setTab('posts')} icon={FileText}>Posts</Tab>
        <Tab active={tab === 'users'} onClick={() => setTab('users')} icon={Users}>Users</Tab>
        <Tab active={tab === 'categories'} onClick={() => setTab('categories')} icon={Tag}>Categories</Tab>
      </div>

      {tab === 'posts' && (
        <div className="space-y-2" data-testid="admin-posts-list">
          {posts.map(p => (
            <div key={p.id} className="border border-[#E4E4E7] bg-white p-4 flex items-center justify-between" data-testid={`admin-post-${p.id}`}>
              <div>
                <p className="font-semibold text-[#050505] text-sm">{p.title}</p>
                <div className="flex gap-2 text-xs text-[#A1A1AA] mt-1">
                  <span className={`px-1.5 ${p.status === 'published' ? 'text-green-600 bg-green-50' : 'text-yellow-600 bg-yellow-50'}`}>{p.status}</span>
                  <span>{p.author?.username}</span>
                </div>
              </div>
              <button onClick={() => deletePost(p.id)} className="text-[#A1A1AA] hover:text-red-500 transition-colors p-2" data-testid={`admin-delete-post-${p.id}`}>
                <Trash2 size={14} />
              </button>
            </div>
          ))}
        </div>
      )}

      {tab === 'users' && (
        <div className="space-y-2" data-testid="admin-users-list">
          {users.map(u => (
            <div key={u.id} className="border border-[#E4E4E7] bg-white p-4 flex items-center justify-between" data-testid={`admin-user-${u.id}`}>
              <div>
                <p className="font-semibold text-[#050505] text-sm">{u.email}</p>
                <p className="text-xs text-[#A1A1AA]">{u.username}</p>
              </div>
              <select value={u.role} onChange={e => updateRole(u.id, e.target.value)}
                className="border border-[#E4E4E7] px-3 py-1.5 text-xs focus:ring-2 focus:ring-[#002FA7] outline-none bg-white"
                data-testid={`user-role-select-${u.id}`}>
                <option value="reader">Reader</option>
                <option value="author">Author</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          ))}
        </div>
      )}

      {tab === 'categories' && (
        <div data-testid="admin-categories">
          <form onSubmit={addCategory} className="flex gap-3 mb-6">
            <input value={newCat} onChange={e => setNewCat(e.target.value)}
              placeholder="New category name..."
              className="flex-1 border border-[#E4E4E7] p-3 text-sm focus:ring-2 focus:ring-[#002FA7] outline-none"
              data-testid="new-category-input" />
            <button type="submit" className="flex items-center gap-2 bg-[#002FA7] text-white px-5 py-3 text-sm hover:bg-[#002280] transition-colors" data-testid="add-category-btn">
              <Plus size={14} /> Add
            </button>
          </form>
          <div className="space-y-2">
            {categories.map(c => (
              <div key={c.id} className="border border-[#E4E4E7] bg-white p-4 flex items-center justify-between" data-testid={`category-item-${c.id}`}>
                <div>
                  <p className="font-medium text-[#050505] text-sm">{c.name}</p>
                  <p className="text-xs text-[#A1A1AA]">{c.post_count} posts</p>
                </div>
                <span className="text-xs text-[#A1A1AA]">/{c.slug}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
