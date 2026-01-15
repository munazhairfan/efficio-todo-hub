import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Protect dashboard and profile routes for unauthenticated users
  if (request.nextUrl.pathname.startsWith('/dashboard') || request.nextUrl.pathname.startsWith('/profile')) {
    // Check if auth token exists in cookies
    const authToken = request.cookies.get('authToken')?.value || null;

    // If no token exists, redirect to auth page
    if (!authToken) {
      return NextResponse.redirect(new URL('/auth', request.url));
    }
  }

  return NextResponse.next();
}

// Apply middleware to protect certain routes
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'], // All routes except API routes and static files
};