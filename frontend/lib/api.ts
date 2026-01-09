// API client for backend communication

import { User, Todo, SignupResponse, SigninResponse, GetUserResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

class ApiClient {
  private baseUrl!: string; // Definite assignment assertion since we throw in constructor if not set

  constructor() {
    // With proxy implementation, we don't need the API_BASE_URL to be set
    // but we'll keep it for logging and potential fallback
    this.baseUrl = API_BASE_URL || '';
    console.log('API Client initialized with base URL:', this.baseUrl || '(using proxy)');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    includeAuth = true
  ): Promise<T> {
    // Use proxy route to avoid mixed content issues with Hugging Face Spaces
    // Construct URL to use our proxy instead of direct backend access
    const normalizedEndpoint = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
    const url = `/api/proxy/${normalizedEndpoint}`;

    console.log('Making API request through proxy:', url);

    // Make sure we have the proper method
    const method = options.method || 'GET';
    const headers = new Headers(options.headers);
    headers.set('Content-Type', 'application/json');

    // Add authorization header if needed and available
    if (includeAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
    }

    try {
      const response = await fetch(url, {
        ...options,
        method, // Ensure method is properly passed
        headers,
      });

      console.log('API response received through proxy:', response.status);

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
      console.error('API request failed for URL:', url, 'Error:', error);
      throw error;
    }
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('authToken');
    }
    return null;
  }

  private setAuthToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', token);
    }
  }

  private removeAuthToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('authToken');
    }
  }

  // Authentication API calls
  async signup(email: string, password: string, name: string): Promise<SignupResponse> {
    return this.request<SignupResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    }, false); // Don't include auth for signup
  }

  async signin(email: string, password: string): Promise<SigninResponse> {
    return this.request<SigninResponse>('/auth/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }, false); // Don't include auth for signin
  }

  async getUser(): Promise<GetUserResponse> {
    return this.request<GetUserResponse>('/profile', {
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
    return this.request<Todo>(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todo),
    });
  }

  async deleteTodo(id: string): Promise<void> {
    await this.request<void>(`/todos/${id}`, {
      method: 'DELETE',
    });
  }
}

export const api = new ApiClient();