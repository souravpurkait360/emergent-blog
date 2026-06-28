import { useState } from 'react';
import useAuthStore from '../store/authStore';
import { format } from 'date-fns';
import { Trash2, Send } from 'lucide-react';
import { toast } from 'sonner';
import client from '../api/client';

export default function CommentSection({ postSlug, comments: initial, onUpdate }) {
  const user = useAuthStore((state) => state.user);
  const [comments, setComments] = useState(initial || []);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);

  const addComment = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    setLoading(true);
    try {
      const { data } = await client.post(`/posts/${postSlug}/comments/`, { content: text });
      setComments(prev => [...prev, data]);
      setText('');
      toast.success('Comment posted');
      if (onUpdate) onUpdate();
    } catch {
      toast.error('Failed to post comment');
    } finally {
      setLoading(false);
    }
  };

  const deleteComment = async (id) => {
    try {
      await client.delete(`/comments/${id}/`);
      setComments(prev => prev.filter(c => c.id !== id));
      toast.success('Comment deleted');
    } catch {
      toast.error('Cannot delete this comment');
    }
  };

  return (
    <div className="mt-12" data-testid="comment-section">
      <h3 className="text-xl font-bold text-[#050505] mb-6" style={{fontFamily:"'Outfit',sans-serif"}}>
        {comments.length} Comment{comments.length !== 1 ? 's' : ''}
      </h3>

      {user && (
        <form onSubmit={addComment} className="mb-8 flex gap-3" data-testid="comment-form">
          <textarea
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="Share your thoughts..."
            rows={3}
            className="flex-1 border border-[#E4E4E7] p-4 text-sm focus:ring-2 focus:ring-[#002FA7] focus:border-transparent resize-none outline-none"
            data-testid="comment-input"
          />
          <button
            type="submit"
            disabled={loading || !text.trim()}
            className="self-end bg-[#002FA7] text-white px-4 py-3 hover:bg-[#002280] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            data-testid="comment-submit-btn"
          >
            <Send size={16} />
          </button>
        </form>
      )}

      <div className="space-y-4">
        {comments.map(c => {
          const authorName = c.author?.first_name
            ? `${c.author.first_name} ${c.author.last_name}`.trim()
            : c.author?.username;
          const canDelete = user && (user.id === c.author?.id || user.role === 'admin');
          return (
            <div key={c.id} className="border border-[#E4E4E7] p-5" data-testid={`comment-${c.id}`}>
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-sm font-semibold text-[#050505]">{authorName}</span>
                  <span className="text-xs text-[#A1A1AA] ml-2">{format(new Date(c.created_at), 'MMM d, yyyy')}</span>
                </div>
                {canDelete && (
                  <button onClick={() => deleteComment(c.id)} className="text-[#A1A1AA] hover:text-red-500 transition-colors" data-testid={`delete-comment-${c.id}`}>
                    <Trash2 size={14} />
                  </button>
                )}
              </div>
              <p className="mt-2 text-sm text-[#52525B]">{c.content}</p>
            </div>
          );
        })}
      </div>

      {!user && (
        <p className="text-sm text-[#52525B] mt-4">
          <a href="/auth" className="text-[#002FA7] hover:underline">Sign in</a> to leave a comment.
        </p>
      )}
    </div>
  );
}
