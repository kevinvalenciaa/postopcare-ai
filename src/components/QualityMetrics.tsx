'use client';

import { CheckCircle, BookOpen, FileCheck, Shield, Star } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { QualityMetrics as QualityMetricsType } from '@/types';

interface QualityMetricsProps {
  metrics: QualityMetricsType;
}

function getScoreColor(score: number): string {
  if (score >= 90) return 'text-green-600';
  if (score >= 75) return 'text-amber-600';
  return 'text-red-600';
}

function getProgressColor(score: number): string {
  if (score >= 90) return 'bg-green-500';
  if (score >= 75) return 'bg-amber-500';
  return 'bg-red-500';
}

export function QualityMetrics({ metrics }: QualityMetricsProps) {
  return (
    <Card className="bg-gray-50">
      <CardContent className="pt-6">
        <div className="mb-4 flex items-center gap-2">
          <Shield className="h-5 w-5 text-blue-600" />
          <h3 className="font-semibold text-gray-900">Quality Score</h3>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {/* Overall Score */}
          <div className="rounded-lg bg-white p-4 shadow-sm">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Star className="h-4 w-4" />
              <span>Overall Score</span>
            </div>
            <div className={`mt-1 text-3xl font-bold ${getScoreColor(metrics.overallScore)}`}>
              {metrics.overallScore}
              <span className="text-lg text-gray-400">/100</span>
            </div>
          </div>

          {/* Readability */}
          <div className="rounded-lg bg-white p-4 shadow-sm">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <BookOpen className="h-4 w-4" />
              <span>Readability</span>
            </div>
            <div className="mt-1">
              <span className={`text-2xl font-bold ${metrics.readabilityGrade <= 8 ? 'text-green-600' : 'text-amber-600'}`}>
                Grade {metrics.readabilityGrade}
              </span>
              <p className="text-xs text-gray-500">Target: 6-8</p>
            </div>
          </div>

          {/* Citation Coverage */}
          <div className="rounded-lg bg-white p-4 shadow-sm">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <FileCheck className="h-4 w-4" />
              <span>Citation Coverage</span>
            </div>
            <div className="mt-2">
              <div className="flex items-center justify-between text-sm">
                <span className={`font-bold ${getScoreColor(metrics.citationCoverage)}`}>
                  {metrics.citationCoverage}%
                </span>
              </div>
              <Progress
                value={metrics.citationCoverage}
                className="mt-1 h-2"
              />
            </div>
          </div>

          {/* Safety Check */}
          <div className="rounded-lg bg-white p-4 shadow-sm">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <CheckCircle className="h-4 w-4" />
              <span>Safety Check</span>
            </div>
            <div className="mt-1 flex items-center gap-2">
              {metrics.safetyCheck === 'passed' ? (
                <>
                  <CheckCircle className="h-6 w-6 text-green-600" />
                  <span className="text-lg font-semibold text-green-600">Passed</span>
                </>
              ) : (
                <>
                  <Shield className="h-6 w-6 text-amber-600" />
                  <span className="text-lg font-semibold text-amber-600">Review</span>
                </>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
