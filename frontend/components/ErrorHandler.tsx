'use client';

import React, { useState, useEffect } from 'react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, Info, XCircle, CheckCircle } from 'lucide-react';

interface ErrorData {
  id?: string;
  message: string;
  type?: 'error' | 'warning' | 'info' | 'success';
  suggestions?: string[];
  canRetry?: boolean;
  errorId?: string;
  handled?: boolean;
}

interface ErrorHandlerProps {
  error: ErrorData | null;
  onRetry?: () => void;
  onDismiss?: () => void;
  autoDismissTimeout?: number; // in milliseconds
  showSuggestions?: boolean;
}

export default function ErrorHandler({
  error,
  onRetry,
  onDismiss,
  autoDismissTimeout = 0,
  showSuggestions = true
}: ErrorHandlerProps) {
  const [isVisible, setIsVisible] = useState(true);
  const [timer, setTimer] = useState<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (error) {
      setIsVisible(true);
      // Set up auto-dismiss timer if specified
      if (autoDismissTimeout > 0) {
        const dismissTimer = setTimeout(() => {
          setIsVisible(false);
        }, autoDismissTimeout);
        setTimer(dismissTimer);
      }
    } else {
      setIsVisible(false);
    }

    // Cleanup timer on unmount or when error changes
    return () => {
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [error, autoDismissTimeout]);

  const handleRetry = () => {
    if (onRetry) {
      onRetry();
    }
    setIsVisible(false);
  };

  const handleDismiss = () => {
    if (onDismiss) {
      onDismiss();
    }
    setIsVisible(false);
  };

  if (!error || !isVisible) {
    return null;
  }

  // Determine icon and styling based on error type
  let IconComponent = AlertCircle;
  let alertVariant: 'default' | 'destructive' = 'default';
  let badgeVariant: 'default' | 'secondary' | 'destructive' | 'outline' = 'default';

  switch (error.type) {
    case 'error':
      IconComponent = XCircle;
      alertVariant = 'destructive';
      badgeVariant = 'destructive';
      break;
    case 'warning':
      IconComponent = AlertCircle;
      alertVariant = 'default';
      badgeVariant = 'default';
      break;
    case 'success':
      IconComponent = CheckCircle;
      alertVariant = 'default';
      badgeVariant = 'default';
      break;
    case 'info':
    default:
      IconComponent = Info;
      alertVariant = 'default';
      badgeVariant = 'secondary';
      break;
  }

  return (
    <Alert variant={alertVariant} className="mb-4 animate-in slide-in-from-top-1 duration-300">
      <IconComponent className="h-4 w-4" />
      <AlertTitle className="flex justify-between items-start">
        <span>
          {(error.type ? error.type.charAt(0).toUpperCase() + error.type.slice(1) : undefined) || 'Info'}
        </span>
        <Button
          variant="ghost"
          size="sm"
          className="h-6 w-6 p-0 hover:bg-transparent"
          onClick={handleDismiss}
        >
          <XCircle className="h-4 w-4" />
        </Button>
      </AlertTitle>
      <AlertDescription>
        <div className="space-y-2">
          <p>{error.message}</p>

          {/* Error ID badge if available */}
          {error.errorId && (
            <Badge variant={badgeVariant} className="text-xs">
              Error ID: {error.errorId}
            </Badge>
          )}

          {/* Suggestions if available and showSuggestions is true */}
          {showSuggestions && error.suggestions && error.suggestions.length > 0 && (
            <div className="mt-3">
              <p className="text-sm font-medium mb-1">Suggestions:</p>
              <ul className="list-disc list-inside space-y-1 text-sm">
                {error.suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Retry button if available and error can be retried */}
          {(error.canRetry || !!onRetry) && (
            <div className="mt-3 flex space-x-2">
              <Button
                size="sm"
                onClick={handleRetry}
                disabled={false}
              >
                Retry
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDismiss}
              >
                Dismiss
              </Button>
            </div>
          )}
        </div>
      </AlertDescription>
    </Alert>
  );
}

// Hook for easier error handling management
export function useErrorHandler() {
  const [error, setError] = useState<ErrorData | null>(null);

  const showError = (errorData: ErrorData) => {
    setError(errorData);
  };

  const hideError = () => {
    setError(null);
  };

  const handleApiError = (apiError: any) => {
    // Extract error information from API response
    const errorInfo: ErrorData = {
      message: apiError.message || 'An unexpected error occurred',
      type: 'error',
      suggestions: apiError.suggestions || ['Please try again later'],
      canRetry: apiError.canRetry || false,
      errorId: apiError.errorId || undefined,
      handled: apiError.handled || undefined
    };

    setError(errorInfo);
  };

  return {
    error,
    showError,
    hideError,
    handleApiError,
    ErrorHandlerComponent: (props?: Partial<ErrorHandlerProps>) => (
      <ErrorHandler
        error={error}
        onDismiss={hideError}
        {...props}
      />
    )
  };
}