'use client';

import { useState, useCallback } from 'react';
import { Header } from '@/components/Header';
import { ProcedureSelect } from '@/components/ProcedureSelect';
import { GenerateButton } from '@/components/GenerateButton';
import { ProgressIndicator } from '@/components/ProgressIndicator';
import { HandoutDisplay } from '@/components/HandoutDisplay';
import { getHandoutByProcedureId, hasHandoutForProcedure } from '@/data/mockHandouts';
import { getProcedureById } from '@/data/procedures';
import { Handout, GENERATION_STEPS } from '@/types';
import { AlertCircle, FileText, Info } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export default function Home() {
  const [selectedProcedure, setSelectedProcedure] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [handout, setHandout] = useState<Handout | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = useCallback(async () => {
    if (!selectedProcedure) return;

    setIsGenerating(true);
    setCurrentStep(0);
    setHandout(null);
    setError(null);

    const apiBase = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
    let cancelled = false;

    // Walk the progress indicator while the API call is in flight.
    const stepTicker = (async () => {
      for (let i = 0; i < GENERATION_STEPS.length - 1; i++) {
        if (cancelled) return;
        setCurrentStep(i);
        await delay(1500 + Math.random() * 1500);
      }
    })();

    try {
      const response = await fetch(`${apiBase}/api/generate-handout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          procedure_id: selectedProcedure,
          section: 'overview',
          top_k: 5,
        }),
      });
      cancelled = true;
      await stepTicker;
      setCurrentStep(GENERATION_STEPS.length - 1);

      if (!response.ok) {
        throw new Error(`API error ${response.status}: ${await response.text()}`);
      }

      const data: Handout = await response.json();
      await delay(200);
      setHandout(data);
    } catch (e) {
      cancelled = true;
      await stepTicker;
      const procedure = getProcedureById(selectedProcedure);
      const message = e instanceof Error ? e.message : String(e);

      // Graceful fallback to mock data when backend isn't reachable.
      if (hasHandoutForProcedure(selectedProcedure)) {
        const mockHandout = getHandoutByProcedureId(selectedProcedure);
        if (mockHandout) {
          setHandout({ ...mockHandout, generatedAt: new Date().toISOString() });
          setError(`Backend unavailable — showing demo content. (${message})`);
        }
      } else {
        setError(
          `Could not generate handout for "${procedure?.name || selectedProcedure}". ${message}`
        );
      }
    } finally {
      setIsGenerating(false);
    }
  }, [selectedProcedure]);

  const canGenerate = selectedProcedure !== null && !isGenerating;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 py-8">
        {/* Selection Area */}
        <div className="mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
                <div className="flex-1">
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    Select Procedure
                  </label>
                  <ProcedureSelect
                    value={selectedProcedure}
                    onValueChange={setSelectedProcedure}
                    disabled={isGenerating}
                  />
                </div>
                <GenerateButton
                  onClick={handleGenerate}
                  disabled={!canGenerate}
                  isLoading={isGenerating}
                />
              </div>

              {/* Info message */}
              {!selectedProcedure && !handout && (
                <div className="mt-4 flex items-start gap-2 rounded-lg bg-blue-50 p-3 text-sm text-blue-700">
                  <Info className="mt-0.5 h-4 w-4 shrink-0" />
                  <p>
                    Select a procedure and click &quot;Generate Handout&quot; to create
                    evidence-based patient instructions. Procedures marked with{' '}
                    <span className="rounded bg-green-100 px-1 text-green-700">
                      Demo
                    </span>{' '}
                    have pre-built content available.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-8">
            <Card className="border-red-200 bg-red-50">
              <CardContent className="pt-6">
                <div className="flex items-start gap-3">
                  <AlertCircle className="h-5 w-5 shrink-0 text-red-600" />
                  <div>
                    <p className="font-medium text-red-800">
                      Handout Not Available
                    </p>
                    <p className="mt-1 text-sm text-red-700">{error}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Progress Indicator */}
        {isGenerating && (
          <div className="mb-8">
            <ProgressIndicator currentStep={currentStep} />
          </div>
        )}

        {/* Generated Handout */}
        {handout && !isGenerating && <HandoutDisplay handout={handout} />}

        {/* Empty State */}
        {!handout && !isGenerating && !error && (
          <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-200 bg-white py-16">
            <FileText className="h-16 w-16 text-gray-300" />
            <h3 className="mt-4 text-lg font-medium text-gray-900">
              No Handout Generated
            </h3>
            <p className="mt-2 text-sm text-gray-500">
              Select a procedure above to generate patient instructions
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t bg-white py-6">
        <div className="container mx-auto px-4">
          <p className="text-center text-sm text-gray-500">
            PostopCare Demo v0.1 — AI-powered post-operative patient education
          </p>
        </div>
      </footer>
    </div>
  );
}
