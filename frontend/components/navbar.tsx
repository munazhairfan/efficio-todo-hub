'use client';

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/components/auth/AuthProvider";
import { useEffect, useState } from "react";

export function Navbar() {
  const { user, loading, signout } = useAuth();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    // Prevent hydration errors by not rendering auth-dependent UI until client-side
    return (
      <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between bg-white/80 backdrop-blur-md border-4 border-black rounded-3xl px-6 py-3 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
          <Link href="/" className="text-2xl font-black italic tracking-tighter text-merlot">
            EFFICIO
          </Link>
          <div className="flex items-center gap-4">
            <Button variant="ghost" className="font-bold text-merlot hover:bg-mint-julep/50" asChild>
              <Link href="/auth">Login</Link>
            </Button>
          </div>
        </div>
      </nav>
    );
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between bg-white/80 backdrop-blur-md border-4 border-black rounded-3xl px-6 py-3 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
        <Link href="/" className="text-2xl font-black italic tracking-tighter text-merlot">
          EFFICIO
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            // User is logged in
            <>
              <span className="hidden md:inline text-merlot font-bold">
                Welcome, {user.name}!
              </span>
              <Button variant="ghost" className="font-bold text-merlot hover:bg-mint-julep/50" asChild>
                <Link href="/dashboard">Dashboard</Link>
              </Button>
              <Button variant="ghost" className="font-bold text-merlot hover:bg-mint-julep/50" asChild>
                <Link href="/profile">Profile</Link>
              </Button>
              <Button
                variant="outline"
                className="font-bold text-merlot border-2 border-merlot hover:bg-merlot hover:text-white"
                onClick={signout}
              >
                Logout
              </Button>
            </>
          ) : (
            // User is not logged in
            <>
              <Button variant="ghost" className="font-bold text-merlot hover:bg-mint-julep/50" asChild>
                <Link href="/auth">Login</Link>
              </Button>
              <Button className="bg-mojo hover:bg-merlot text-white font-black border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl" asChild>
                <Link href="/auth">GET STARTED</Link>
              </Button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
