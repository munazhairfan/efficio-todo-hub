'use client';

import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertTriangle, CheckCircle, Clock, ShieldAlert } from 'lucide-react';

interface ConfirmationDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => Promise<void> | void;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  variant?: 'default' | 'destructive' | 'warning' | 'info';
  countdownSeconds?: number; // Optional countdown before confirmation is enabled
  showCancel?: boolean;
}

export default function ConfirmationDialog({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = "Confirm",
  cancelText = "Cancel",
  variant = 'default',
  countdownSeconds = 0,
  showCancel = true
}: ConfirmationDialogProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [countdown, setCountdown] = useState(countdownSeconds);
  const [isCountdownActive, setIsCountdownActive] = useState(false);

  useEffect(() => {
    if (isOpen && countdownSeconds > 0) {
      setIsCountdownActive(true);
      setCountdown(countdownSeconds);
    } else {
      setIsCountdownActive(false);
      setCountdown(0);
    }
  }, [isOpen, countdownSeconds]);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (isCountdownActive && countdown > 0) {
      interval = setInterval(() => {
        setCountdown(prev => prev - 1);
      }, 1000);
    } else if (countdown === 0 && isCountdownActive) {
      setIsCountdownActive(false);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isCountdownActive, countdown]);

  const handleConfirm = async () => {
    if (isLoading) return;

    setIsLoading(true);
    try {
      await onConfirm();
      handleClose();
    } catch (error) {
      console.error('Confirmation failed:', error);
      // Optionally handle error, show notification, etc.
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setIsLoading(false);
    onClose();
    // Reset countdown if dialog is closed
    if (countdown !== countdownSeconds) {
      setCountdown(countdownSeconds);
    }
  };

  // Determine icon and styling based on variant
  let IconComponent = CheckCircle;
  let alertVariant: 'default' | 'destructive' = 'default';
  let alertClass = '';

  switch (variant) {
    case 'destructive':
      IconComponent = AlertTriangle;
      alertVariant = 'destructive';
      alertClass = 'border-red-200 bg-red-50';
      break;
    case 'warning':
      IconComponent = AlertTriangle;
      alertVariant = 'default';
      alertClass = 'border-yellow-200 bg-yellow-50';
      break;
    case 'info':
      IconComponent = Clock;
      alertVariant = 'default';
      alertClass = 'border-blue-200 bg-blue-50';
      break;
    default:
      IconComponent = ShieldAlert;
      alertClass = 'border-gray-200 bg-gray-50';
  }

  const isConfirmDisabled = isCountdownActive && countdown > 0;

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <IconComponent className={`h-5 w-5 ${
              variant === 'destructive' ? 'text-red-600' :
              variant === 'warning' ? 'text-yellow-600' :
              variant === 'info' ? 'text-blue-600' : 'text-gray-600'
            }`} />
            {title}
          </DialogTitle>
        </DialogHeader>

        <Alert variant={alertVariant} className={alertClass}>
          <AlertDescription>
            {message}
          </AlertDescription>
        </Alert>

        {isCountdownActive && countdown > 0 && (
          <div className="text-center py-2">
            <p className="text-sm text-muted-foreground">
              Confirmation enabled in {countdown} second{countdown !== 1 ? 's' : ''}
            </p>
          </div>
        )}

        <div className="flex justify-end space-x-2 pt-2">
          {showCancel && (
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isLoading}
            >
              {cancelText}
            </Button>
          )}

          <Button
            type="button"
            onClick={handleConfirm}
            disabled={isConfirmDisabled || isLoading}
            variant={variant === 'destructive' ? 'destructive' : 'default'}
          >
            {isLoading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : (
              <>
                {isConfirmDisabled ? 'Waiting...' : confirmText}
                {variant === 'destructive' && (
                  <span className="ml-2">(Irreversible)</span>
                )}
              </>
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

// Convenience hook for managing confirmation dialogs
export function useConfirmationDialog() {
  const [isOpen, setIsOpen] = useState(false);
  const [dialogProps, setDialogProps] = useState<Omit<ConfirmationDialogProps, 'isOpen' | 'onClose'>>({
    title: '',
    message: '',
    onConfirm: () => {},
    variant: 'default'
  });

  const showConfirmation = (
    props: Omit<ConfirmationDialogProps, 'isOpen' | 'onClose'>
  ) => {
    setDialogProps(props);
    setIsOpen(true);
  };

  const hideConfirmation = () => {
    setIsOpen(false);
  };

  return {
    ConfirmationDialog: (
      <ConfirmationDialog
        isOpen={isOpen}
        onClose={hideConfirmation}
        {...dialogProps}
      />
    ),
    showConfirmation,
    hideConfirmation,
    isOpen
  };
}