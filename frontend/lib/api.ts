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
    let url = `${cleanBaseUrl}/api${normalizedEndpoint}`;

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

    // Special handling for Hugging Face Spaces which may redirect HTTPS to HTTP
    // If we detect the Hugging Face domain and HTTPS, try with HTTP first
    if (url.includes('hf.space') && url.startsWith('https://')) {
      console.warn('Detected Hugging Face Space with HTTPS - attempting to use HTTP instead to avoid redirect issues');
      url = url.replace('https://', 'http://');
      console.log('Updated URL to:', url);
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      console.log('API response received:', response.url, response.status, 'Redirected:', response.redirected);

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

      // If the error persists and we're using Hugging Face with HTTPS, try alternative approach
      if (url.includes('hf.space') && url.startsWith('https://')) {
        const httpUrl = url.replace('https://', 'http://');
        console.warn('Retrying with HTTP URL due to Hugging Face Space compatibility:', httpUrl);

        try {
          const response = await fetch(httpUrl, {
            ...options,
            headers,
          });

          console.log('Fallback HTTP request succeeded:', response.url, response.status);

          if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API request failed: ${response.status} ${response.statusText}`);
          }

          // Handle 204 No Content responses
          if (response.status === 204) {
            return {} as T;
          }

          return response.json();
        } catch (fallbackError) {
          console.error('Fallback HTTP request also failed:', fallbackError);
          throw error; // Throw the original error
        }
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