// API client for backend communication

import { User, Todo, SignupResponse, SigninResponse, GetUserResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

class ApiClient {
  private baseUrl!: string; // Definite assignment assertion since we throw in constructor if not set

  constructor() {
    if (!API_BASE_URL) {
      throw new Error('NEXT_PUBLIC_API_URL is not set. Please configure the environment variable.');
    }

    this.baseUrl = API_BASE_URL;
    console.log('API Client initialized with base URL:', this.baseUrl);
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    includeAuth = true
  ): Promise<T> {
    // Remove trailing slash from baseUrl if it exists to prevent double slashes
    const cleanBaseUrl = this.baseUrl.endsWith('/') ? this.baseUrl.slice(0, -1) : this.baseUrl;
    // Ensure endpoint starts with a slash for consistent URL construction
    const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    const url = `${cleanBaseUrl}/api${normalizedEndpoint}`;

    console.log('Making API request to URL:', url);

    const headers = new Headers(options.headers);
    headers.set('Content-Type', 'application/json');

    // Add authorization header if needed and available
    if (includeAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
    }

    // Handle potential redirects from HTTPS to HTTP by catching the error and retrying with HTTP
    // This addresses the issue where Hugging Face Spaces sometimes redirect HTTPS to HTTP
    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      console.log('API response received:', response.url, response.status, 'Redirected:', response.redirected);

      if (response.redirected && response.url.startsWith('http://')) {
        console.warn('API request was redirected from HTTPS to HTTP. This may cause mixed content issues.', url, '->', response.url);

        // If it was redirected to HTTP, we should handle this appropriately
        if (url.startsWith('https://') && response.url.startsWith('http://')) {
          console.error('Mixed content detected: attempted HTTPS but was redirected to HTTP');
          throw new Error(`Mixed content error: API request to ${url} was redirected to insecure HTTP endpoint ${response.url}. This violates browser security policies.`);
        }
      }

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

      // If the error is related to mixed content or HTTPS redirect to HTTP, log this specifically
      if (url.startsWith('https://') && error instanceof TypeError && error.message.includes('Failed to fetch')) {
        console.warn('HTTPS request failed - this might be due to the server redirecting to HTTP');
      }

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