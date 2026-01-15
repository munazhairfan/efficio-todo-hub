// Utilities for loading and error state management

export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  message?: string;
  canRetry: boolean;
}

export const createStateUtils = () => {
  // Loading state utilities
  const setLoadingState = (isLoading: boolean, message?: string): LoadingState => ({
    isLoading,
    message
  });

  const startLoading = (message?: string): LoadingState => ({
    isLoading: true,
    message: message || 'Processing...'
  });

  const stopLoading = (): LoadingState => ({
    isLoading: false
  });

  // Error state utilities
  const setErrorState = (hasError: boolean, message?: string, canRetry = true): ErrorState => ({
    hasError,
    message,
    canRetry
  });

  const showError = (message: string, canRetry = true): ErrorState => ({
    hasError: true,
    message,
    canRetry
  });

  const hideError = (): ErrorState => ({
    hasError: false,
    canRetry: true
  });

  return {
    setLoadingState,
    startLoading,
    stopLoading,
    setErrorState,
    showError,
    hideError
  };
};

export const defaultLoadingState: LoadingState = {
  isLoading: false
};

export const defaultErrorState: ErrorState = {
  hasError: false,
  canRetry: true
};