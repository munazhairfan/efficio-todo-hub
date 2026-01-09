import { NextRequest } from 'next/server';

// Generic handler that works for all HTTP methods
async function handleRequest(request: NextRequest, path: string, method: string) {
  const searchParams = request.nextUrl.search;
  const backendUrl = `http://munazha-efficio-todo-hub.hf.space/api/${path}${searchParams}`;

  try {
    let body = null;
    if (method !== 'GET' && method !== 'HEAD') {
      body = await request.json().catch(() => null);
    }

    const authToken = request.headers.get('authorization');

    const response = await fetch(backendUrl, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': authToken } : {}),
      },
      ...(body && { body: JSON.stringify(body) }),
    });

    // Clone the response to read the body
    const responseBody = await response.text();

    return new Response(responseBody, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
        // Forward any other important headers
        ...Object.fromEntries(response.headers.entries()),
      },
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return new Response(JSON.stringify({ error: 'Proxy error', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function GET(request: NextRequest, { params }: { params: { path: string } }) {
  const { path } = params;
  return handleRequest(request, path, 'GET');
}

export async function POST(request: NextRequest, { params }: { params: { path: string } }) {
  const { path } = params;
  return handleRequest(request, path, 'POST');
}

export async function PUT(request: NextRequest, { params }: { params: { path: string } }) {
  const { path } = params;
  return handleRequest(request, path, 'PUT');
}

export async function PATCH(request: NextRequest, { params }: { params: { path: string } }) {
  const { path } = params;
  return handleRequest(request, path, 'PATCH');
}

export async function DELETE(request: NextRequest, { params }: { params: { path: string } }) {
  const { path } = params;
  return handleRequest(request, path, 'DELETE');
}

export async function HEAD(request: NextRequest, { params }: { params: { path: string } }) {
  const { path } = params;
  return handleRequest(request, path, 'HEAD');
}