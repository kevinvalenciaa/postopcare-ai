'use client';

import { useRef } from 'react';
import { FileText, Calendar, Printer, Copy, Check } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { SectionCard } from './SectionCard';
import { CitationsList } from './CitationsList';
import { QualityMetrics } from './QualityMetrics';
import { Handout } from '@/types';
import { useState } from 'react';

interface HandoutDisplayProps {
  handout: Handout;
}

export function HandoutDisplay({ handout }: HandoutDisplayProps) {
  const [copied, setCopied] = useState(false);
  const citationsRef = useRef<HTMLDivElement>(null);

  const handleCitationClick = (citationId: number) => {
    citationsRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handlePrint = () => {
    window.print();
  };

  const handleCopy = async () => {
    // Create plain text version of the handout
    const textContent = handout.sections
      .map((section) => {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = section.content;
        return `## ${section.title}\n\n${tempDiv.textContent || tempDiv.innerText}`;
      })
      .join('\n\n---\n\n');

    const fullText = `${handout.title}\n\n${textContent}`;

    try {
      await navigator.clipboard.writeText(fullText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const formattedDate = new Date(handout.generatedAt).toLocaleDateString(
    'en-US',
    {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-r from-blue-600 to-blue-700 text-white">
        <CardHeader>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-4">
              <div className="rounded-lg bg-white/10 p-3">
                <FileText className="h-8 w-8" />
              </div>
              <div>
                <CardTitle className="text-2xl font-bold text-white">
                  {handout.title}
                </CardTitle>
                <div className="mt-1 flex items-center gap-2 text-sm text-blue-100">
                  <Calendar className="h-4 w-4" />
                  <span>Generated {formattedDate}</span>
                </div>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                variant="secondary"
                size="sm"
                onClick={handleCopy}
                className="bg-white/10 text-white hover:bg-white/20"
              >
                {copied ? (
                  <Check className="mr-2 h-4 w-4" />
                ) : (
                  <Copy className="mr-2 h-4 w-4" />
                )}
                {copied ? 'Copied!' : 'Copy'}
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={handlePrint}
                className="bg-white/10 text-white hover:bg-white/20"
              >
                <Printer className="mr-2 h-4 w-4" />
                Print
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Quality Metrics */}
      <QualityMetrics metrics={handout.qualityMetrics} />

      {/* Sections */}
      <div className="space-y-4">
        {handout.sections.map((section, index) => (
          <SectionCard
            key={section.id}
            section={section}
            defaultOpen={index === 0}
            onCitationClick={handleCitationClick}
          />
        ))}
      </div>

      {/* Citations */}
      <div ref={citationsRef}>
        <CitationsList citations={handout.citations} />
      </div>
    </div>
  );
}
