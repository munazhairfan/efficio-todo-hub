// API client for backend communication

import { User, Todo, SignupResponse, SigninResponse, GetUserResponse } from '@/types';

// Define types for our conversation robustness API responses
export interface ConversationClarificationResponse {
  responseType: 'clarification' | 'success' | 'error';
  message: string;
  clarifyingQuestions: string[];
  suggestedActions: string[];
  conversationId: string | null;
  analysis?: {
    intent: any;
    ambiguity: any;
    vagueness: any;
  };
}

export interface ConversationStateResponse {
  id: string;
  session_id: string;
  current_intent: string | null;
  pending_clarifications: string[];
  context_data: Record<string, any>;
  created_at: string;
  updated_at: string;
  expires_at: string;
}

export interface ErrorResponse {
  userMessage: string;
  suggestedActions: string[];
  canRetry: boolean;
  errorId: string;
  handled: boolean;
}

class ApiClient {
  constructor() {
    console.log('API Client initialized with Vercel API routes');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    includeAuth = true
  ): Promise<T> {
    // Use Vercel API routes directly
    const url = `/api${endpoint}`;

    // Make sure we have the proper method
    const method = options.method || 'GET';
    const headers = new Headers(options.headers);
    headers.set('Content-Type', 'application/json');

    // Include Authorization header with JWT token if available
    if (includeAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
    }

    try {
      const response = await fetch(`${url}`, {  // Fixed: was using undefined 'url' variable
        ...options,
        method, // Ensure method is properly passed
        headers,
      });

      console.log('API response received:', response.status);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `API request failed: ${response.status} ${response.statusText}`);
      }

      // Handle 204 No Content responses
      if (response.status === 204) {
        return {} as T;
      }

      return response.json();
    } catch (error) {
      console.error('API request failed for URL:', `${url}`, 'Error:', error);  // Fixed: was using undefined 'url' variable
      throw error;
    }
  }

  // Helper method to get the auth token from cookies or localStorage
  private getAuthToken(): string | null {
    // First try to get from document.cookie (browser)
    if (typeof document !== 'undefined') {
      const cookies = document.cookie.split(';');
      for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'authToken') {
          return value;
        }
      }
    }

    // Fallback to localStorage for client-side storage
    if (typeof window !== 'undefined' && window.localStorage) {
      const token = window.localStorage.getItem('authToken');
      if (token) {
        return token;
      }
    }

    // For server-side rendering, we might need to get it differently
    // But in client-side this should work
    return null;
  }

  // Authentication API calls
  async signup(email: string, password: string, name: string): Promise<SignupResponse> {
    return this.request<SignupResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    }); // Auth is handled by cookies in the API routes
  }

  async signin(email: string, password: string): Promise<SigninResponse> {
    return this.request<SigninResponse>('/auth/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }); // Auth is handled by cookies in the API routes
  }

  async getUser(): Promise<GetUserResponse> {
    return this.request<GetUserResponse>('/users', {
      method: 'GET',
    });
  }

  // Todo API calls
  async getTodos(): Promise<{ todos: Todo[] }> {
    return this.request<{ todos: Todo[] }>('/todos', {
      method: 'GET',
    });
  }

  async createTodo(todo: Omit<Todo, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<Todo> {
    return this.request<Todo>('/todos', {
      method: 'POST',
      body: JSON.stringify(todo),
    });
  }

  async updateTodo(id: string, todo: Partial<Todo>): Promise<Todo> {
    // Update with query param for ID
    return this.request<Todo>('/todos', {
      method: 'PUT',
      body: JSON.stringify({ ...todo, id }),
    });
  }

  async deleteTodo(id: string): Promise<void> {
    // Delete with query param for ID
    await this.request<void>(`/todos?id=${encodeURIComponent(id)}`, {
      method: 'DELETE',
    });
  }

  // Conversation API methods
  async clarifyConversation(
    sessionId: string,
    userInput: string,
    context: Record<string, any> = {}
  ): Promise<ConversationClarificationResponse> {
    return this.request<ConversationClarificationResponse>('/conversation/clarify', {
      method: 'POST',
      body: JSON.stringify({
        sessionId,
        input: userInput,
        context
      })
    });
  }

  async getConversationState(sessionId: string): Promise<ConversationStateResponse> {
    return this.request<ConversationStateResponse>(`/conversation/state/${sessionId}`, {
      method: 'GET'
    });
  }

  async updateConversationState(
    sessionId: string,
    updateData: Partial<ConversationStateResponse>
  ): Promise<ConversationStateResponse> {
    return this.request<ConversationStateResponse>(`/conversation/state/${sessionId}`, {
      method: 'POST',
      body: JSON.stringify(updateData)
    });
  }

  async deleteConversationState(sessionId: string): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/conversation/state/${sessionId}`, {
      method: 'DELETE'
    });
  }

  async analyzeInput(input: string): Promise<any> {
    return this.request<any>('/conversation/analyze-input', {
      method: 'POST',
      body: JSON.stringify({ input })
    });
  }

  // Error handling API methods
  async handleError(
    errorType: string,
    originalRequest: Record<string, any>,
    technicalDetails?: string
  ): Promise<ErrorResponse> {
    return this.request<ErrorResponse>('/error/handle', {
      method: 'POST',
      body: JSON.stringify({
        errorType,
        originalRequest,
        technicalDetails
      })
    });
  }

  async getError(errorId: string): Promise<ErrorResponse> {
    return this.request<ErrorResponse>(`/error/${errorId}`, {
      method: 'GET'
    });
  }

  async markErrorAsHandled(errorId: string): Promise<ErrorResponse> {
    return this.request<ErrorResponse>(`/error/${errorId}/mark-handled`, {
      method: 'PUT'
    });
  }

  // Chat API method
  async sendMessage(userId: string, message: string, conversationId?: string) {
    const requestBody: any = {
      message,
      context: {
        user_id: userId
      }
    };

    if (conversationId) {
      requestBody.conversation_id = conversationId;
    }

    return this.request<any>('chat', {
      method: 'POST',
      body: JSON.stringify(requestBody)
    });
  }

  // Utility method to get a new session ID (using UUID v4 format)
  generateSessionId(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}

// Export the main API client
export const api = new ApiClient();

// Create and export specialized API interfaces for different functionality
export const conversationApi = {
  clarify: api.clarifyConversation.bind(api),
  getState: api.getConversationState.bind(api),
  updateState: api.updateConversationState.bind(api),
  deleteState: api.deleteConversationState.bind(api),
  analyzeInput: api.analyzeInput.bind(api)
};

export const errorApi = {
  handle: api.handleError.bind(api),
  get: api.getError.bind(api),
  markAsHandled: api.markErrorAsHandled.bind(api)
};