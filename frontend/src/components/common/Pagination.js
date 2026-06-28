export default function Pagination({ currentPage, totalCount, pageSize = 9, onPageChange }) {
  const totalPages = Math.ceil(totalCount / pageSize);
  if (totalPages <= 1) return null;

  return (
    <div className="flex justify-center items-center gap-2 mt-12" data-testid="pagination">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="px-4 py-2 border border-edge text-sm disabled:opacity-30 hover:border-accent hover:text-accent transition-colors"
      >
        Prev
      </button>
      <span className="px-4 py-2 text-sm text-ink-muted">
        Page {currentPage} of {totalPages}
      </span>
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage >= totalPages}
        className="px-4 py-2 border border-edge text-sm disabled:opacity-30 hover:border-accent hover:text-accent transition-colors"
      >
        Next
      </button>
    </div>
  );
}
