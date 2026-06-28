export default function SkeletonCard() {
  return (
    <div className="bg-surface border border-edge" aria-hidden="true">
      <div className="h-44 skeleton" />
      <div className="p-6 space-y-3">
        <div className="h-3 w-16 skeleton" />
        <div className="h-5 w-full skeleton" />
        <div className="h-4 w-3/4 skeleton" />
        <div className="h-3 w-1/2 skeleton" />
      </div>
    </div>
  );
}
