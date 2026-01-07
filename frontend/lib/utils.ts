import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Error handling utilities
export class ApiError extends Error {
  public readonly status: number;
  public readonly data?: any;

  constructor(message: string, status: number, data?: any) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = 'ApiError';
  }
}

export const handleApiError = (error: any): ApiError => {
  if (error instanceof ApiError) {
    return error;
  }

  if (error.status) {
    return new ApiError(error.message || 'API request failed', error.status, error.data);
  }

  if (error.message) {
    return new ApiError(error.message, 500);
  }

  return new ApiError('An unknown error occurred', 500);
};

// Toast notification utilities
export const showErrorToast = (message: string) => {
  if (typeof window !== 'undefined') {
    // Using react-hot-toast if available, or fallback to console.error
    console.error(message);
  }
};

export const showSuccessToast = (message: string) => {
  if (typeof window !== 'undefined') {
    console.log(message);
  }
};

// Form validation utilities
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePassword = (password: string): boolean => {
  // Password must be at least 8 characters
  return password.length >= 8;
};

export const validateName = (name: string): boolean => {
  // Name must be between 1 and 100 characters
  return name.length >= 1 && name.length <= 100;
};