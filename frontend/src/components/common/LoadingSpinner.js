export default function LoadingSpinner() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-canvas">
      <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" data-testid="loading-spinner" />
    </div>
  );
}
