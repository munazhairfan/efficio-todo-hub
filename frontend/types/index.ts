// Shared TypeScript type definitions

export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

export interface AuthToken {
  token: string;
  expiration: string; // ISO date string
  userId: string;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  success: boolean;
}

// Authentication API response types
export interface SignupResponse {
  user: User;
  token: string;
}

export interface SigninResponse {
  user: User;
  token: string;
}

export interface GetUserResponse {
  id: string;
  email: string;
  name: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}