import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Currently no server-side authentication logic needed
  // Authentication is handled client-side in components using localStorage
  return NextResponse.next();
}

// Apply middleware to all routes if needed in the future
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'], // All routes except API routes and static files
};