import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { MessageSquare, Eye } from 'lucide-react';

const DEFAULT_COVERS = [
  'https://images.unsplash.com/photo-1531591022136-eb8b0da1e6d0?w=800&q=80',
  'https://images.pexels.com/photos/12696432/pexels-photo-12696432.jpeg?w=800',
  'https://images.unsplash.com/photo-1567943183748-3a7542120c90?w=800&q=80',
];

export default function PostCard({ post, index = 0, large = false }) {
  const cover = post.cover_image_url || DEFAULT_COVERS[index % 3];
  const authorName = post.author?.first_name
    ? `${post.author.first_name} ${post.author.last_name}`.trim()
    : post.author?.username || 'Anonymous';

  return (
    <Link to={`/post/${post.slug}`} data-testid={`post-card-${post.id}`} className="group block bg-white border border-[#E4E4E7] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300">
      <div className={`overflow-hidden ${large ? 'h-72' : 'h-44'}`}>
        <img
          src={cover}
          alt={post.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
      </div>
      <div className="p-6">
        {post.category && (
          <span className="text-xs tracking-[0.2em] uppercase font-bold text-[#002FA7]">
            {post.category.name}
          </span>
        )}
        <h3 className={`mt-2 font-bold text-[#050505] leading-tight group-hover:text-[#002FA7] transition-colors ${large ? 'text-2xl' : 'text-lg'}`} style={{fontFamily:"'Outfit',sans-serif"}}>
          {post.title}
        </h3>
        {post.ai_summary && (
          <p className="mt-2 text-sm text-[#52525B] line-clamp-2">{post.ai_summary}</p>
        )}
        <div className="mt-4 flex items-center justify-between text-xs text-[#A1A1AA]">
          <span>{authorName} · {post.created_at ? format(new Date(post.created_at), 'MMM d') : ''}</span>
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1"><Eye size={12} />{post.views}</span>
            <span className="flex items-center gap-1"><MessageSquare size={12} />{post.comment_count}</span>
          </div>
        </div>
        {post.tags?.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {post.tags.slice(0, 3).map(t => (
              <span key={t.id} className="text-xs px-2 py-0.5 bg-[#F4F4F5] text-[#52525B]">#{t.name}</span>
            ))}
          </div>
        )}
      </div>
    </Link>
  );
}
