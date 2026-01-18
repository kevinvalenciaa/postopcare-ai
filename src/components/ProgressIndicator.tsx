'use client';

import { Check, Loader2, Circle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { GENERATION_STEPS } from '@/types';
import { cn } from '@/lib/utils';

interface ProgressIndicatorProps {
  currentStep: number;
  isComplete?: boolean;
}

export function ProgressIndicator({
  currentStep,
  isComplete = false,
}: ProgressIndicatorProps) {
  const progressPercentage = isComplete
    ? 100
    : Math.round((currentStep / GENERATION_STEPS.length) * 100);

  return (
    <Card className="border-blue-200 bg-blue-50/50">
      <CardContent className="pt-6">
        <div className="mb-4">
          <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span className="font-medium">Generating handout...</span>
            <span>{progressPercentage}%</span>
          </div>
          <Progress value={progressPercentage} className="h-2" />
        </div>

        <div className="space-y-3">
          {GENERATION_STEPS.map((step, index) => {
            const status =
              isComplete || index < currentStep
                ? 'completed'
                : index === currentStep
                  ? 'in-progress'
                  : 'pending';

            return (
              <div key={step.id} className="flex items-center gap-3">
                <div
                  className={cn(
                    'flex h-6 w-6 items-center justify-center rounded-full transition-colors',
                    status === 'completed' && 'bg-green-500 text-white',
                    status === 'in-progress' && 'bg-blue-500 text-white',
                    status === 'pending' && 'bg-gray-200 text-gray-400'
                  )}
                >
                  {status === 'completed' ? (
                    <Check className="h-4 w-4" />
                  ) : status === 'in-progress' ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Circle className="h-3 w-3" />
                  )}
                </div>
                <span
                  className={cn(
                    'text-sm transition-colors',
                    status === 'completed' && 'text-green-700',
                    status === 'in-progress' && 'text-blue-700 font-medium',
                    status === 'pending' && 'text-gray-400'
                  )}
                >
                  {step.label}
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
