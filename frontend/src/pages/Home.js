import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Search } from 'lucide-react';
import PostCard from '../components/PostCard';
import client from '../api/client';

const HERO_IMG = 'https://images.pexels.com/photos/21325139/pexels-photo-21325139.jpeg?auto=compress&cs=tinysrgb&w=1600';

function SkeletonCard() {
  return (
    <div className="bg-white border border-[#E4E4E7]">
      <div className="h-44 skeleton" />
      <div className="p-6 space-y-3">
        <div className="h-3 w-16 skeleton" />
        <div className="h-5 skeleton" />
        <div className="h-4 w-3/4 skeleton" />
      </div>
    </div>
  );
}

export default function Home() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [activeCategory, setActiveCategory] = useState(searchParams.get('category') || '');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const fetchPosts = async () => {
    setLoading(true);
    try {
      const params = { page };
      if (search) params.search = search;
      if (activeCategory) params['category__slug'] = activeCategory;
      const { data } = await client.get('/posts/', { params });
      setPosts(data.results || data);
      setTotal(data.count || 0);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  useEffect(() => {
    client.get('/categories/').then(r => setCategories(r.data.results || r.data || []));
  }, []);

  useEffect(() => {
    setPage(1);
    fetchPosts();
  }, [search, activeCategory]);

  useEffect(() => { fetchPosts(); }, [page]);

  const handleSearch = (e) => {
    e.preventDefault();
    const val = e.target.elements.search?.value || '';
    setSearch(val);
    setSearchParams(val ? { search: val } : {});
  };

  const featured = posts[0];
  const rest = posts.slice(1);

  return (
    <main>
      {/* Hero */}
      <section className="relative h-[70vh] min-h-[500px] overflow-hidden" data-testid="hero-section">
        <img src={HERO_IMG} alt="Hero" className="absolute inset-0 w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent" />
        <div className="absolute inset-0 flex flex-col justify-end p-8 md:p-16 max-w-4xl">
          <motion.p
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="text-xs tracking-[0.3em] uppercase font-bold text-zinc-300 mb-3"
          >
            The Modern Writing Platform
          </motion.p>
          <motion.h1
            initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="text-5xl sm:text-6xl font-black tracking-tighter text-white leading-none mb-6"
            style={{fontFamily:"'Outfit',sans-serif"}}
          >
            IDEAS WORTH<br />READING
          </motion.h1>
          <motion.form
            onSubmit={handleSearch}
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="flex max-w-md"
          >
            <input
              name="search"
              defaultValue={search}
              placeholder="Search posts..."
              className="flex-1 bg-white/10 backdrop-blur-sm border border-white/30 text-white placeholder-white/60 px-4 py-3 text-sm focus:outline-none focus:border-white"
              data-testid="hero-search-input"
            />
            <button type="submit" className="bg-[#002FA7] text-white px-6 py-3 hover:bg-[#002280] transition-colors" data-testid="hero-search-btn">
              <Search size={18} />
            </button>
          </motion.form>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Category Filter */}
        <div className="flex gap-2 flex-wrap mb-10" data-testid="category-filters">
          <button
            onClick={() => setActiveCategory('')}
            className={`px-4 py-2 text-sm border transition-colors ${!activeCategory ? 'bg-[#002FA7] text-white border-[#002FA7]' : 'border-[#E4E4E7] text-[#52525B] hover:border-[#002FA7] hover:text-[#002FA7]'}`}
            data-testid="category-all-btn"
          >
            All
          </button>
          {categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.slug)}
              className={`px-4 py-2 text-sm border transition-colors ${activeCategory === cat.slug ? 'bg-[#002FA7] text-white border-[#002FA7]' : 'border-[#E4E4E7] text-[#52525B] hover:border-[#002FA7] hover:text-[#002FA7]'}`}
              data-testid={`category-${cat.slug}-btn`}
            >
              {cat.name}
            </button>
          ))}
        </div>

        {/* Post Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => <SkeletonCard key={i} />)}
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-24" data-testid="empty-state">
            <p className="text-[#52525B] text-lg">No posts found.</p>
            <Link to="/write" className="mt-4 inline-block text-[#002FA7] underline text-sm">Write the first one</Link>
          </div>
        ) : (
          <>
            {/* Bento Grid */}
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6 mb-6">
              {featured && (
                <div className="md:col-span-8">
                  <PostCard post={featured} index={0} large />
                </div>
              )}
              {rest[0] && (
                <div className="md:col-span-4">
                  <PostCard post={rest[0]} index={1} />
                </div>
              )}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {rest.slice(1).map((p, i) => (
                <motion.div
                  key={p.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                >
                  <PostCard post={p} index={i + 2} />
                </motion.div>
              ))}
            </div>

            {/* Pagination */}
            {total > 9 && (
              <div className="flex justify-center gap-2 mt-12" data-testid="pagination">
                <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
                  className="px-4 py-2 border border-[#E4E4E7] text-sm disabled:opacity-30 hover:border-[#002FA7] hover:text-[#002FA7] transition-colors">
                  Prev
                </button>
                <span className="px-4 py-2 text-sm text-[#52525B]">Page {page} of {Math.ceil(total / 9)}</span>
                <button onClick={() => setPage(p => p + 1)} disabled={page >= Math.ceil(total / 9)}
                  className="px-4 py-2 border border-[#E4E4E7] text-sm disabled:opacity-30 hover:border-[#002FA7] hover:text-[#002FA7] transition-colors">
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </main>
  );
}
