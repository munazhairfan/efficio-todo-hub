import { NextRequest } from 'next/server';

// Handle all HTTP methods in a single route handler
export async function GET(request: NextRequest) {
  const url = new URL(request.url);
  const endpoint = url.searchParams.get('endpoint') || '';
  const backendUrl = `http://munazha-efficio-todo-hub.hf.space/api/${endpoint}`;

  try {
    const authToken = request.headers.get('authorization');

    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': authToken } : {}),
      },
    });

    const responseBody = await response.text();

    return new Response(responseBody, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
        ...Object.fromEntries(response.headers.entries()),
      },
    });
  } catch (error) {
    console.error('Proxy GET error:', error);
    return new Response(JSON.stringify({ error: 'Proxy error', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function POST(request: NextRequest) {
  const url = new URL(request.url);
  const endpoint = url.searchParams.get('endpoint') || '';
  const backendUrl = `http://munazha-efficio-todo-hub.hf.space/api/${endpoint}`;

  try {
    const body = await request.json().catch(() => ({}));
    const authToken = request.headers.get('authorization');

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': authToken } : {}),
      },
      body: JSON.stringify(body),
    });

    const responseBody = await response.text();

    return new Response(responseBody, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
        ...Object.fromEntries(response.headers.entries()),
      },
    });
  } catch (error) {
    console.error('Proxy POST error:', error);
    return new Response(JSON.stringify({ error: 'Proxy error', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function PUT(request: NextRequest) {
  const url = new URL(request.url);
  const endpoint = url.searchParams.get('endpoint') || '';
  const backendUrl = `http://munazha-efficio-todo-hub.hf.space/api/${endpoint}`;

  try {
    const body = await request.json().catch(() => ({}));
    const authToken = request.headers.get('authorization');

    const response = await fetch(backendUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': authToken } : {}),
      },
      body: JSON.stringify(body),
    });

    const responseBody = await response.text();

    return new Response(responseBody, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
        ...Object.fromEntries(response.headers.entries()),
      },
    });
  } catch (error) {
    console.error('Proxy PUT error:', error);
    return new Response(JSON.stringify({ error: 'Proxy error', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function DELETE(request: NextRequest) {
  const url = new URL(request.url);
  const endpoint = url.searchParams.get('endpoint') || '';
  const backendUrl = `http://munazha-efficio-todo-hub.hf.space/api/${endpoint}`;

  try {
    const authToken = request.headers.get('authorization');

    const response = await fetch(backendUrl, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': authToken } : {}),
      },
    });

    const responseBody = await response.text();

    return new Response(responseBody, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
        ...Object.fromEntries(response.headers.entries()),
      },
    });
  } catch (error) {
    console.error('Proxy DELETE error:', error);
    return new Response(JSON.stringify({ error: 'Proxy error', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}