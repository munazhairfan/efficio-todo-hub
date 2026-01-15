'use client';

import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface ClarificationDialogProps {
  isOpen: boolean;
  onClose: () => void;
  questions: string[];
  onSubmit: (answer: string) => void;
  title?: string;
}

export default function ClarificationDialog({
  isOpen,
  onClose,
  questions,
  onSubmit,
  title = "Need Clarification"
}: ClarificationDialogProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Reset to first question when dialog opens
    if (isOpen) {
      setCurrentQuestionIndex(0);
      setUserAnswer('');
    }
  }, [isOpen]);

  const handleAnswerChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserAnswer(e.target.value);
  };

  const handleSubmit = async () => {
    if (!userAnswer.trim()) return;

    setIsLoading(true);
    try {
      await onSubmit(userAnswer);
      // Move to next question or close if done
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(prev => prev + 1);
        setUserAnswer('');
      } else {
        onClose();
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
      // Optionally show error to user
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkip = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setUserAnswer('');
    } else {
      onClose();
    }
  };

  if (questions.length === 0) return null;

  const currentQuestion = questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === questions.length - 1;
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Question {currentQuestionIndex + 1} of {questions.length}
            </span>
            <span className="text-sm text-gray-500">
              {Math.round(progress)}%
            </span>
          </div>

          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>

          <div className="mt-4">
            <Label htmlFor="clarification-answer" className="text-base font-medium">
              {currentQuestion}
            </Label>
            <Input
              id="clarification-answer"
              value={userAnswer}
              onChange={handleAnswerChange}
              placeholder="Type your answer here..."
              disabled={isLoading}
              autoFocus
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSubmit();
                }
              }}
            />
          </div>
        </div>

        <div className="flex justify-between pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={handleSkip}
            disabled={isLoading}
          >
            Skip
          </Button>

          <div className="flex space-x-2">
            {!isLastQuestion && (
              <Button
                type="button"
                variant="outline"
                onClick={handleSkip}
                disabled={isLoading}
              >
                Next
              </Button>
            )}

            <Button
              type="button"
              onClick={handleSubmit}
              disabled={!userAnswer.trim() || isLoading}
            >
              {isLoading ? 'Processing...' : isLastQuestion ? 'Submit' : 'Continue'}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}