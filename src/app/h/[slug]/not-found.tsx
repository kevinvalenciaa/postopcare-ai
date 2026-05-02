import Link from 'next/link';
import { FileX2 } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="flex flex-col items-center text-center">
        <FileX2 className="h-16 w-16 text-gray-300" />
        <h1 className="mt-4 text-xl font-semibold text-gray-900">
          Handout not found
        </h1>
        <p className="mt-2 max-w-md text-sm text-gray-600">
          This handout may have been removed or the link may be incorrect. Please ask your clinician for an updated link.
        </p>
        <Link
          href="/"
          className="mt-6 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Generate a new handout
        </Link>
      </div>
    </div>
  );
}
