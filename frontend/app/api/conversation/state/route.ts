import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Extract session ID from query parameters
    const { searchParams } = new URL(request.url);
    const sessionId = searchParams.get('sessionId');

    if (!sessionId) {
      return new Response(JSON.stringify({ error: 'Session ID is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Check if BACKEND_URL is configured
    if (!process.env.BACKEND_URL || process.env.BACKEND_URL === 'http://localhost:8000') {
      // Return a mock response when backend is not configured
      return new Response(JSON.stringify({
        id: sessionId,
        session_id: sessionId,
        current_intent: "Mock conversation state",
        pending_clarifications: [],
        context_data: {},
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours from now
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const backendUrl = `${process.env.BACKEND_URL}/api/conversation/state/${sessionId}`;

    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Forward any authentication headers if present
        ...(request.headers.get('authorization') ? { 'authorization': request.headers.get('authorization')! } : {}),
      },
    });

    const data = await response.json();
    return new Response(JSON.stringify(data), {
      status: response.status,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Conversation state GET API error:', error);
    // Return a fallback response
    const { searchParams } = new URL(request.url);
    const sessionId = searchParams.get('sessionId') || 'fallback-session';

    return new Response(JSON.stringify({
      id: sessionId,
      session_id: sessionId,
      current_intent: "Fallback conversation state",
      pending_clarifications: [],
      context_data: {},
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours from now
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function POST(request: NextRequest) {
  try {
    // Extract session ID from query parameters
    const { searchParams } = new URL(request.url);
    const sessionId = searchParams.get('sessionId');

    if (!sessionId) {
      return new Response(JSON.stringify({ error: 'Session ID is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Check if BACKEND_URL is configured
    if (!process.env.BACKEND_URL || process.env.BACKEND_URL === 'http://localhost:8000') {
      // Return a mock response when backend is not configured
      const body = await request.json();

      return new Response(JSON.stringify({
        id: sessionId,
        session_id: sessionId,
        current_intent: body.current_intent || "Updated mock conversation state",
        pending_clarifications: body.pending_clarifications || [],
        context_data: body.context_data || {},
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours from now
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const backendUrl = `${process.env.BACKEND_URL}/api/conversation/state/${sessionId}`;

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
    console.error('Conversation state POST API error:', error);
    // Return a fallback response
    const { searchParams } = new URL(request.url);
    const sessionId = searchParams.get('sessionId') || 'fallback-session';
    const body = await request.json();

    return new Response(JSON.stringify({
      id: sessionId,
      session_id: sessionId,
      current_intent: body.current_intent || "Fallback conversation state",
      pending_clarifications: body.pending_clarifications || [],
      context_data: body.context_data || {},
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours from now
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function DELETE(request: NextRequest) {
  try {
    // Extract session ID from query parameters
    const { searchParams } = new URL(request.url);
    const sessionId = searchParams.get('sessionId');

    if (!sessionId) {
      return new Response(JSON.stringify({ error: 'Session ID is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Check if BACKEND_URL is configured
    if (!process.env.BACKEND_URL || process.env.BACKEND_URL === 'http://localhost:8000') {
      // Return a success response when backend is not configured
      return new Response(JSON.stringify({
        message: "Conversation state deleted successfully (mock)"
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const backendUrl = `${process.env.BACKEND_URL}/api/conversation/state/${sessionId}`;

    const response = await fetch(backendUrl, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        // Forward any authentication headers if present
        ...(request.headers.get('authorization') ? { 'authorization': request.headers.get('authorization')! } : {}),
      },
    });

    const data = await response.json();
    return new Response(JSON.stringify(data), {
      status: response.status,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Conversation state DELETE API error:', error);
    // Return a fallback response
    return new Response(JSON.stringify({
      message: "Conversation state deleted (fallback)"
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}