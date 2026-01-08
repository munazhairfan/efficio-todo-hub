'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { auth } from '@/lib/auth';
import { User } from '@/types';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  signin: (email: string, password: string) => Promise<{ user: User; token: string }>;
  signup: (email: string, password: string, name: string) => Promise<{ user: User; token: string }>;
  signout: () => void;
  getCurrentUser: () => Promise<User>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Sync auth token between localStorage and cookies for server-side access
  useEffect(() => {
    // Only run this effect on the client side
    if (typeof window === 'undefined' || typeof document === 'undefined') {
      return;
    }

    // Function to sync localStorage token to cookies
    const syncTokenToCookie = (token: string | null) => {
      // Set the token in a cookie that expires in 24 hours
      if (token) {
        document.cookie = `authToken=${token}; path=/; max-age=${24 * 60 * 60}; samesite=strict`;
      } else {
        // Clear the cookie if no token
        document.cookie = 'authToken=; path=/; max-age=0; samesite=strict';
      }
    };

    // On initial load, sync the existing token if any
    const existingToken = localStorage.getItem('authToken');
    if (existingToken) {
      syncTokenToCookie(existingToken);
    }

    // Listen for storage events to sync changes across tabs
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'authToken') {
        syncTokenToCookie(e.newValue);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  useEffect(() => {
    // Check if user is authenticated on initial load
    const checkAuthStatus = async () => {
      try {
        if (auth.isAuthenticated()) {
          const userData = await auth.getCurrentUser();
          setUser(userData);
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        // If there's an error, clear the token
        auth.signout();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const signin = async (email: string, password: string) => {
    console.log('AuthProvider signin called with:', { email });
    try {
      const response = await auth.signin(email, password);
      console.log('AuthProvider signin response:', response);

      // Sync token to cookies after successful signin
      if (response.token && typeof window !== 'undefined' && typeof document !== 'undefined') {
        document.cookie = `authToken=${response.token}; path=/; max-age=${24 * 60 * 60}; samesite=strict`;
      }

      setUser(response.user);
      console.log('User state updated in AuthProvider');
      return response;
    } catch (error) {
      console.error('AuthProvider signin error:', error);
      throw error;
    }
  };

  const signup = async (email: string, password: string, name: string) => {
    console.log('AuthProvider signup called with:', { email, name });
    try {
      const response = await auth.signup(email, password, name);
      console.log('AuthProvider signup response:', response);

      // Sync token to cookies after successful signup
      if (response.token && typeof window !== 'undefined' && typeof document !== 'undefined') {
        document.cookie = `authToken=${response.token}; path=/; max-age=${24 * 60 * 60}; samesite=strict`;
      }

      setUser(response.user);
      console.log('User state updated in AuthProvider');
      return response;
    } catch (error) {
      console.error('AuthProvider signup error:', error);
      throw error;
    }
  };

  const signout = () => {
    auth.signout();
    // Clear cookie on signout
    if (typeof window !== 'undefined' && typeof document !== 'undefined') {
      document.cookie = 'authToken=; path=/; max-age=0; samesite=strict';
    }
    setUser(null);
  };

  const getCurrentUser = async () => {
    const userData = await auth.getCurrentUser();
    setUser(userData);
    return userData;
  };

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: !loading && !!user, // Only authenticated if loaded AND user exists
    signin,
    signup,
    signout,
    getCurrentUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}