import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const backendUrl = `${process.env.BACKEND_URL || 'http://localhost:8000'}/api/conversation/analyze-input`;

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
    console.error('Conversation analyze-input API error:', error);
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}