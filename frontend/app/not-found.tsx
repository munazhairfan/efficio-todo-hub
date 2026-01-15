'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-mint-julep to-confetti p-4">
      <div className="text-center max-w-md">
        <div className="text-8xl font-black text-merlot mb-4">404</div>
        <h1 className="text-3xl font-bold text-merlot mb-4">Page Not Found</h1>
        <p className="text-lg text-mojo mb-8">
          Oops! The page you're looking for doesn't exist or has been moved.
        </p>
        <Link href="/" passHref>
          <Button className="h-12 bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl">
            Go Back Home
          </Button>
        </Link>
      </div>
    </div>
  );
}