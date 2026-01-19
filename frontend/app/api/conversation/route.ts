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

    // Check if BACKEND_URL is configured
    if (!process.env.BACKEND_URL || process.env.BACKEND_URL === 'http://localhost:8000') {
      // Return a mock response when backend is not configured
      const body = await request.json();

      // Mock response for conversation endpoints
      if (endpoint.includes('analyze-input')) {
        const userInput = body.input || "";
        const hasAmbiguity = userInput.toLowerCase().includes("what") || userInput.toLowerCase().includes("how");

        return new Response(JSON.stringify({
          input: userInput,
          analysis: {
            intent: { is_ambiguous: hasAmbiguity },
            ambiguity: { is_ambiguous: hasAmbiguity },
            vagueness: { is_vague: userInput.length < 5 }
          },
          needs_clarification: hasAmbiguity,
          clarifying_questions: hasAmbiguity ? ["Could you provide more details?"] : [],
          handled_locally: false
        }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }

      return new Response(JSON.stringify({
        error: 'Backend service not configured',
        message: 'Conversation service is not available'
      }), {
        status: 503,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const backendUrl = `${process.env.BACKEND_URL}/api/conversation/${endpoint}`;

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
    // Return a fallback response
    const { pathname } = new URL(request.url);
    const pathParts = pathname.split('/api/conversation/');
    const endpoint = pathParts[1] || '';

    if (endpoint.includes('analyze-input')) {
      const body = await request.json();
      const userInput = body.input || "";

      return new Response(JSON.stringify({
        input: userInput,
        analysis: {
          intent: { is_ambiguous: false },
          ambiguity: { is_ambiguous: false },
          vagueness: { is_vague: false }
        },
        needs_clarification: false,
        clarifying_questions: [],
        handled_locally: false
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({
      error: 'Service temporarily unavailable',
      message: 'Conversation service is temporarily down, please try again later'
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}