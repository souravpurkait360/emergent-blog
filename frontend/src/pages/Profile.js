import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { Edit, Eye, FileText } from 'lucide-react';
import { motion } from 'framer-motion';
import useAuthStore from '../store/authStore';
import client from '../api/client';

export default function Profile() {
  const user = useAuthStore((state) => state.user);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    client.get('/posts/my/')
      .then(r => setPosts(r.data.results || r.data))
      .finally(() => setLoading(false));
  }, []);

  const published = posts.filter(p => p.status === 'published');
  const drafts = posts.filter(p => p.status === 'draft');

  return (
    <div className="max-w-5xl mx-auto px-6 py-12" data-testid="profile-page">
      {/* User Info */}
      <div className="border border-[#E4E4E7] bg-white p-8 mb-10 flex flex-col md:flex-row gap-6 items-start">
        <div className="w-16 h-16 bg-[#002FA7] rounded-none flex items-center justify-center text-white text-2xl font-black shrink-0" style={{fontFamily:"'Outfit',sans-serif"}}>
          {user?.first_name?.charAt(0) || user?.email?.charAt(0).toUpperCase()}
        </div>
        <div className="flex-1">
          <h1 className="text-2xl font-black text-[#050505]" style={{fontFamily:"'Outfit',sans-serif"}}>
            {user?.first_name ? `${user.first_name} ${user.last_name}` : user?.username}
          </h1>
          <p className="text-sm text-[#52525B] mt-1">{user?.email}</p>
          <div className="flex items-center gap-4 mt-4 text-sm text-[#52525B]">
            <span className="px-2 py-0.5 bg-[#F4F4F5] uppercase text-xs font-bold tracking-wider">{user?.role}</span>
            <span>{published.length} posts published</span>
            <span>{drafts.length} drafts</span>
          </div>
        </div>
        <Link to="/write" className="bg-[#002FA7] text-white px-5 py-2.5 text-sm hover:bg-[#002280] transition-colors shrink-0" data-testid="new-post-btn">
          New Post
        </Link>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-10">
        {[
          { label: 'Published', val: published.length, icon: Eye },
          { label: 'Drafts', val: drafts.length, icon: FileText },
          { label: 'Total Views', val: posts.reduce((s, p) => s + p.views, 0), icon: Eye },
        ].map(({ label, val, icon: Icon }) => (
          <div key={label} className="border border-[#E4E4E7] bg-white p-6 text-center">
            <p className="text-3xl font-black text-[#002FA7]" style={{fontFamily:"'Outfit',sans-serif"}}>{val}</p>
            <p className="text-xs uppercase tracking-wider text-[#52525B] mt-1">{label}</p>
          </div>
        ))}
      </div>

      {/* Posts */}
      <h2 className="text-xl font-bold text-[#050505] mb-4" style={{fontFamily:"'Outfit',sans-serif"}}>My Posts</h2>
      {loading ? (
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => <div key={i} className="h-20 skeleton" />)}
        </div>
      ) : posts.length === 0 ? (
        <div className="border border-[#E4E4E7] p-12 text-center">
          <p className="text-[#52525B]">No posts yet.</p>
          <Link to="/write" className="mt-3 inline-block text-[#002FA7] underline text-sm">Write your first post</Link>
        </div>
      ) : (
        <div className="space-y-3" data-testid="my-posts-list">
          {posts.map((p, i) => (
            <motion.div key={p.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.04 }}
              className="border border-[#E4E4E7] bg-white p-5 flex items-center justify-between gap-4"
              data-testid={`my-post-${p.id}`}>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-[#050505] truncate">{p.title}</h3>
                <div className="flex items-center gap-3 text-xs text-[#A1A1AA] mt-1">
                  <span className={`px-1.5 py-0.5 uppercase font-bold ${p.status === 'published' ? 'bg-green-50 text-green-700' : 'bg-yellow-50 text-yellow-700'}`}>
                    {p.status}
                  </span>
                  {p.created_at && <span>{format(new Date(p.created_at), 'MMM d, yyyy')}</span>}
                  <span className="flex items-center gap-1"><Eye size={10} /> {p.views}</span>
                </div>
              </div>
              <div className="flex gap-2">
                <Link to={`/post/${p.slug}`} className="p-2 border border-[#E4E4E7] hover:border-[#002FA7] text-[#52525B] hover:text-[#002FA7] transition-colors" data-testid={`view-post-${p.id}`}>
                  <Eye size={14} />
                </Link>
                <Link to={`/write/${p.slug}`} className="p-2 border border-[#E4E4E7] hover:border-[#002FA7] text-[#52525B] hover:text-[#002FA7] transition-colors" data-testid={`edit-post-${p.id}`}>
                  <Edit size={14} />
                </Link>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
