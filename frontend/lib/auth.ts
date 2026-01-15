// Authentication utilities

import { api } from './api';
import { User } from '@/types';

class AuthUtils {
  // Helper function to set auth token in cookies
  private setAuthTokenInCookies(token: string | null) {
    if (typeof window !== 'undefined' && typeof document !== 'undefined') {
      if (token) {
        // Set the token in a cookie that expires in 24 hours
        document.cookie = `authToken=${token}; path=/; max-age=${24 * 60 * 60}; samesite=strict`;
      } else {
        // Clear the cookie if no token
        document.cookie = 'authToken=; path=/; max-age=0; samesite=strict';
      }
    }
  }

  // Sign up a new user
  async signup(email: string, password: string, name: string): Promise<{ user: User; token: string }> {
    const response = await api.signup(email, password, name);

    // Store the token in localStorage and cookies
    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', response.token);
      this.setAuthTokenInCookies(response.token);
    }

    return response;
  }

  // Sign in an existing user
  async signin(email: string, password: string): Promise<{ user: User; token: string }> {
    const response = await api.signin(email, password);

    // Store the token in localStorage and cookies
    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', response.token);
      this.setAuthTokenInCookies(response.token);
    }

    return response;
  }

  // Get current user info
  async getCurrentUser(): Promise<User> {
    return await api.getUser();
  }

  // Sign out the current user
  signout() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('authToken');
      this.setAuthTokenInCookies(null);
    }
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('authToken');
      // In a real implementation, you might want to check token expiration
      return !!token;
    }
    return false;
  }

  // Get the authentication token
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('authToken');
    }
    return null;
  }
}

export const auth = new AuthUtils();