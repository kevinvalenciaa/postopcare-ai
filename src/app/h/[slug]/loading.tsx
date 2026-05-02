export default function Loading() {
  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto max-w-3xl px-4 py-6 sm:py-10">
        <div className="h-32 animate-pulse rounded-lg bg-gradient-to-r from-blue-200 to-blue-300" />
        <div className="mt-6 space-y-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-20 animate-pulse rounded-lg bg-white" />
          ))}
        </div>
      </main>
    </div>
  );
}
