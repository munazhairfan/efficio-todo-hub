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