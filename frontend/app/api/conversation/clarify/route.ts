import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Check if BACKEND_URL is configured
    if (!process.env.BACKEND_URL || process.env.BACKEND_URL === 'http://localhost:8000') {
      // Return a mock response when backend is not configured
      const body = await request.json();

      // Simple analysis - in a real implementation, this would be more sophisticated
      const userInput = body.input || body.message || "";
      const hasAmbiguity = userInput.toLowerCase().includes("what") || userInput.toLowerCase().includes("how") || userInput.toLowerCase().includes("where");

      const mockResponse = {
        responseType: hasAmbiguity ? 'clarification' : 'success',
        message: hasAmbiguity
          ? "I can help clarify that for you. Could you provide more details?"
          : `I understood your request: "${userInput}". How can I assist you further?`,
        clarifyingQuestions: hasAmbiguity
          ? [`Could you elaborate on what you mean by "${userInput.split(' ').slice(0, 3).join(' ')}"?`, "What specifically are you looking for?"]
          : [],
        suggestedActions: [],
        conversationId: body.sessionId || `conv_${Date.now()}`,
        analysis: {
          intent: { is_ambiguous: hasAmbiguity },
          ambiguity: { is_ambiguous: hasAmbiguity },
          vagueness: { is_vague: userInput.length < 5 }
        }
      };

      return new Response(JSON.stringify(mockResponse), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const backendUrl = `${process.env.BACKEND_URL}/api/conversation/clarify`;

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
    console.error('Conversation clarify API error:', error);
    // Return a fallback response when backend fails
    const body = await request.json();
    const userInput = body.input || body.message || "";

    const fallbackResponse = {
      responseType: 'success',
      message: `I received your message: "${userInput}". The AI service is temporarily unavailable, but I'm working on it.`,
      clarifyingQuestions: ["Is there anything specific you'd like me to help with?"],
      suggestedActions: [],
      conversationId: body.sessionId || `conv_${Date.now()}`,
      analysis: {
        intent: { is_ambiguous: false },
        ambiguity: { is_ambiguous: false },
        vagueness: { is_vague: false }
      }
    };

    return new Response(JSON.stringify(fallbackResponse), {
      status: 200, // Return 200 instead of 500 to prevent error display
      headers: { 'Content-Type': 'application/json' },
    });
  }
}