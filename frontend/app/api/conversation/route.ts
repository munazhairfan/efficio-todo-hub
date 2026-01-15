import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Extract the API route and session ID from the URL
    const { pathname } = new URL(request.url);
    const pathParts = pathname.split('/api/conversation/');
    if (pathParts.length < 2) {
      return new Response(JSON.stringify({ error: 'Invalid API path' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const endpoint = pathParts[1];
    const backendUrl = `${process.env.BACKEND_URL || 'http://localhost:8000'}/api/conversation/${endpoint}`;

    // Forward the request to the backend
    const body = await request.json();
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Forward any authentication headers if present
        ...(request.headers.get('authorization') ? { 'authorization': request.headers.get('authorization')! } : {}),
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return new Response(JSON.stringify(data), {
      status: response.status,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Conversation API error:', error);
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}