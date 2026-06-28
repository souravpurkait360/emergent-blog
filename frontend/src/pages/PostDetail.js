import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { Eye, Edit, Trash2, ArrowLeft, Tag } from 'lucide-react';
import { motion } from 'framer-motion';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';
import CommentSection from '../components/CommentSection';
import client from '../api/client';

const DEFAULT_COVER = 'https://images.unsplash.com/photo-1531591022136-eb8b0da1e6d0?w=1200&q=80';

export default function PostDetail() {
  const { slug } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    client.get(`/posts/${slug}/`)
      .then(r => setPost(r.data))
      .catch(() => navigate('/'))
      .finally(() => setLoading(false));
  }, [slug]);

  const handleDelete = async () => {
    if (!window.confirm('Delete this post?')) return;
    try {
      await client.delete(`/posts/${slug}/`);
      toast.success('Post deleted');
      navigate('/');
    } catch { toast.error('Cannot delete this post'); }
  };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-[#002FA7] border-t-transparent rounded-full animate-spin" />
    </div>
  );

  if (!post) return null;

  const canEdit = user && (user.id === post.author?.id || user.role === 'admin');
  const authorName = post.author?.first_name
    ? `${post.author.first_name} ${post.author.last_name}`.trim()
    : post.author?.username;

  return (
    <motion.article initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="max-w-4xl mx-auto px-6 py-12" data-testid="post-detail">
      <Link to="/" className="flex items-center gap-2 text-sm text-[#52525B] hover:text-[#002FA7] mb-8 transition-colors">
        <ArrowLeft size={16} /> Back to posts
      </Link>

      {/* Header */}
      <header className="mb-10">
        {post.category && (
          <span className="text-xs tracking-[0.2em] uppercase font-bold text-[#002FA7]">{post.category.name}</span>
        )}
        <h1 className="mt-3 text-4xl sm:text-5xl font-black tracking-tighter text-[#050505] leading-tight" style={{fontFamily:"'Outfit',sans-serif"}} data-testid="post-title">
          {post.title}
        </h1>
        <div className="mt-6 flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3 text-sm text-[#52525B]">
            <div className="w-8 h-8 bg-[#002FA7] rounded-full flex items-center justify-center text-white text-xs font-bold">
              {authorName?.charAt(0).toUpperCase()}
            </div>
            <div>
              <span className="font-medium text-[#050505]">{authorName}</span>
              <span className="mx-2">·</span>
              {post.created_at && format(new Date(post.created_at), 'MMMM d, yyyy')}
            </div>
            <span className="flex items-center gap-1 text-xs"><Eye size={12} /> {post.views}</span>
          </div>
          {canEdit && (
            <div className="flex gap-2">
              <Link to={`/write/${post.slug}`} className="flex items-center gap-1.5 px-3 py-1.5 border border-[#E4E4E7] text-xs hover:border-[#002FA7] hover:text-[#002FA7] transition-colors" data-testid="edit-post-btn">
                <Edit size={12} /> Edit
              </Link>
              <button onClick={handleDelete} className="flex items-center gap-1.5 px-3 py-1.5 border border-[#E4E4E7] text-xs hover:border-red-500 hover:text-red-500 transition-colors" data-testid="delete-post-btn">
                <Trash2 size={12} /> Delete
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Cover Image */}
      {(post.cover_image_url) && (
        <div className="w-full h-72 md:h-96 overflow-hidden mb-10">
          <img src={post.cover_image_url || DEFAULT_COVER} alt={post.title} className="w-full h-full object-cover" />
        </div>
      )}

      {/* AI Summary */}
      {post.ai_summary && (
        <div className="mb-10 bg-[#002FA7] text-white p-6 border-l-4 border-white/30" data-testid="ai-summary-block">
          <p className="text-xs tracking-[0.2em] uppercase font-bold mb-2" style={{fontFamily:"'JetBrains Mono',monospace"}}>AI Summary</p>
          <p className="text-sm leading-relaxed opacity-90">{post.ai_summary}</p>
        </div>
      )}

      {/* Content */}
      <div
        className="post-content"
        dangerouslySetInnerHTML={{ __html: post.content }}
        data-testid="post-content"
      />

      {/* Tags */}
      {post.tags?.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-10 pt-8 border-t border-[#E4E4E7]" data-testid="post-tags">
          <Tag size={14} className="text-[#A1A1AA] mt-1" />
          {post.tags.map(t => (
            <span key={t.id} className="px-3 py-1 bg-[#F4F4F5] text-sm text-[#52525B]">#{t.name}</span>
          ))}
        </div>
      )}

      {/* Comments */}
      <div className="mt-8 pt-8 border-t border-[#E4E4E7]">
        <CommentSection
          postSlug={slug}
          comments={post.comments || []}
          onUpdate={() => client.get(`/posts/${slug}/`).then(r => setPost(r.data))}
        />
      </div>
    </motion.article>
  );
}
