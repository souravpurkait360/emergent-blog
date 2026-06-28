import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Bold, Italic, Heading1, Heading2, List, Link2, Quote, Sparkles, Loader } from 'lucide-react';
import { toast } from 'sonner';
import client from '../api/client';

function ToolbarBtn({ icon: Icon, cmd, val, title }) {
  const exec = () => { document.execCommand(cmd, false, val || null); };
  return (
    <button type="button" onMouseDown={e => { e.preventDefault(); exec(); }}
      title={title}
      className="p-2 text-[#52525B] hover:text-[#002FA7] hover:bg-[#F4F4F5] transition-colors"
    >
      <Icon size={16} />
    </button>
  );
}

export default function PostEditor() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const editorRef = useRef(null);
  const [title, setTitle] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [tagInput, setTagInput] = useState('');
  const [categories, setCategories] = useState([]);
  const [coverFile, setCoverFile] = useState(null);
  const [aiSummary, setAiSummary] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [postId, setPostId] = useState(null);

  useEffect(() => {
    client.get('/categories/').then(r => setCategories(r.data.results || r.data || []));
    if (slug) {
      client.get(`/posts/${slug}/`).then(r => {
        const p = r.data;
        setTitle(p.title);
        setCategoryId(p.category?.id || '');
        setTagInput(p.tags?.map(t => t.name).join(', ') || '');
        setAiSummary(p.ai_summary || '');
        setPostId(p.id);
        if (editorRef.current) editorRef.current.innerHTML = p.content || '';
      });
    }
  }, [slug]);

  const getContent = () => editorRef.current?.innerHTML || '';

  const handleAIAssist = async () => {
    if (!title && !getContent()) return toast.error('Add some content first');
    setAiLoading(true);
    try {
      const { data } = await client.post('/ai/assist/', {
        content: getContent(),
        prompt: `Continue writing this blog post titled "${title}". Return only the continuation HTML:`,
      });
      if (editorRef.current && data.suggestion) {
        editorRef.current.innerHTML += `<p>${data.suggestion}</p>`;
        toast.success('AI content added!');
      }
    } catch { toast.error('AI assist failed'); }
    finally { setAiLoading(false); }
  };

  const handleAISummarize = async () => {
    if (!getContent()) return toast.error('Add content first');
    setAiLoading(true);
    try {
      const { data } = await client.post('/ai/summarize/', { title, content: getContent() });
      setAiSummary(data.summary || '');
      toast.success('Summary generated!');
    } catch { toast.error('AI summarize failed'); }
    finally { setAiLoading(false); }
  };

  const handleSave = async (status) => {
    if (!title.trim()) return toast.error('Title is required');
    setSaving(true);
    try {
      const form = new FormData();
      form.append('title', title);
      form.append('content', getContent());
      form.append('status', status);
      if (categoryId) form.append('category_id', categoryId);
      if (aiSummary) form.append('ai_summary', aiSummary);
      if (coverFile) form.append('cover_image', coverFile);
      const tags = tagInput.split(',').map(t => t.trim()).filter(Boolean);
      tags.forEach(t => form.append('tag_names', t));

      if (slug) {
        await client.patch(`/posts/${slug}/`, form, { headers: { 'Content-Type': 'multipart/form-data' } });
        toast.success('Post updated!');
        navigate(`/post/${slug}`);
      } else {
        const { data } = await client.post('/posts/', form, { headers: { 'Content-Type': 'multipart/form-data' } });
        toast.success('Post created!');
        navigate(`/post/${data.slug}`);
      }
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Save failed');
    } finally { setSaving(false); }
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-10" data-testid="post-editor">
      <h1 className="text-3xl font-black tracking-tight mb-8 text-[#050505]" style={{fontFamily:"'Outfit',sans-serif"}}>
        {slug ? 'Edit Post' : 'New Post'}
      </h1>

      {/* Title */}
      <input
        value={title}
        onChange={e => setTitle(e.target.value)}
        placeholder="Post title..."
        className="w-full text-3xl font-bold border-0 border-b-2 border-[#E4E4E7] focus:border-[#002FA7] outline-none pb-4 mb-8 bg-transparent"
        style={{fontFamily:"'Outfit',sans-serif"}}
        data-testid="post-title-input"
      />

      {/* Meta fields */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <select value={categoryId} onChange={e => setCategoryId(e.target.value)}
          className="border border-[#E4E4E7] p-3 text-sm focus:ring-2 focus:ring-[#002FA7] outline-none bg-white"
          data-testid="category-select">
          <option value="">No Category</option>
          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <input value={tagInput} onChange={e => setTagInput(e.target.value)}
          placeholder="Tags: tech, writing, ai"
          className="border border-[#E4E4E7] p-3 text-sm focus:ring-2 focus:ring-[#002FA7] outline-none md:col-span-2"
          data-testid="tags-input"
        />
      </div>

      {/* Cover Image */}
      <div className="mb-6">
        <label className="text-xs tracking-[0.2em] uppercase font-bold text-[#52525B] block mb-2">Cover Image</label>
        <input type="file" accept="image/*" onChange={e => setCoverFile(e.target.files[0])}
          className="text-sm text-[#52525B] file:mr-4 file:py-2 file:px-4 file:border-0 file:bg-[#002FA7] file:text-white file:text-sm file:cursor-pointer hover:file:bg-[#002280]"
          data-testid="cover-image-input"
        />
        {coverFile && <p className="text-xs text-[#52525B] mt-1">{coverFile.name}</p>}
      </div>

      {/* Toolbar */}
      <div className="border border-[#E4E4E7] border-b-0 flex items-center gap-1 px-2 py-1 bg-[#FAFAFA] flex-wrap">
        <ToolbarBtn icon={Bold} cmd="bold" title="Bold" />
        <ToolbarBtn icon={Italic} cmd="italic" title="Italic" />
        <ToolbarBtn icon={Heading1} cmd="formatBlock" val="H1" title="Heading 1" />
        <ToolbarBtn icon={Heading2} cmd="formatBlock" val="H2" title="Heading 2" />
        <ToolbarBtn icon={List} cmd="insertUnorderedList" title="List" />
        <ToolbarBtn icon={Quote} cmd="formatBlock" val="blockquote" title="Quote" />
        <div className="flex-1" />
        <button type="button" onClick={handleAIAssist} disabled={aiLoading}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-[#002FA7] text-white text-xs hover:bg-[#002280] disabled:opacity-50 transition-colors"
          data-testid="ai-assist-btn">
          {aiLoading ? <Loader size={12} className="animate-spin" /> : <Sparkles size={12} />}
          AI Write
        </button>
        <button type="button" onClick={handleAISummarize} disabled={aiLoading}
          className="flex items-center gap-1.5 px-3 py-1.5 border border-[#002FA7] text-[#002FA7] text-xs hover:bg-[#002FA7] hover:text-white disabled:opacity-50 transition-colors"
          data-testid="ai-summarize-btn">
          <Sparkles size={12} />
          AI Summary
        </button>
      </div>

      {/* Editor */}
      <div
        ref={editorRef}
        contentEditable
        suppressContentEditableWarning
        className="rich-editor border border-[#E4E4E7] p-6 min-h-[400px] focus:ring-2 focus:ring-[#002FA7]"
        data-testid="post-content-editor"
        placeholder="Start writing..."
      />

      {/* AI Summary */}
      {aiSummary && (
        <div className="mt-4 p-4 bg-[#002FA7]/5 border border-[#002FA7]/20" data-testid="ai-summary-preview">
          <p className="text-xs tracking-[0.2em] uppercase font-bold text-[#002FA7] mb-1">AI Summary Preview</p>
          <textarea
            value={aiSummary}
            onChange={e => setAiSummary(e.target.value)}
            rows={3}
            className="w-full text-sm bg-transparent outline-none text-[#52525B] resize-none"
          />
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3 mt-6" data-testid="editor-actions">
        <button onClick={() => handleSave('draft')} disabled={saving}
          className="px-6 py-3 border border-[#E4E4E7] text-sm hover:border-[#050505] transition-colors disabled:opacity-50"
          data-testid="save-draft-btn">
          {saving ? 'Saving...' : 'Save Draft'}
        </button>
        <button onClick={() => handleSave('published')} disabled={saving}
          className="px-6 py-3 bg-[#002FA7] text-white text-sm hover:bg-[#002280] transition-colors disabled:opacity-50"
          data-testid="publish-btn">
          {saving ? 'Publishing...' : 'Publish'}
        </button>
      </div>
    </div>
  );
}
