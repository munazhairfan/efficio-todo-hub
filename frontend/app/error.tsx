'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-mint-julep to-confetti p-4">
      <div className="text-center max-w-md">
        <div className="text-6xl font-black text-red-500 mb-4">⚠️</div>
        <h1 className="text-3xl font-bold text-merlot mb-4">Something went wrong!</h1>
        <p className="text-lg text-mojo mb-8">
          An unexpected error occurred. Please try again or contact support if the issue persists.
        </p>
        <div className="flex flex-col gap-4">
          <Button
            onClick={() => reset()}
            className="h-12 bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl"
          >
            Try Again
          </Button>
          <Link href="/" passHref>
            <Button variant="outline" className="h-12 border-2 border-merlot text-merlot hover:bg-merlot hover:text-white">
              Go Back Home
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}