'use client';

import { BookOpen, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Citation } from '@/types';

interface CitationsListProps {
  citations: Citation[];
}

function formatAmaCitation(citation: Citation): string {
  let formatted = `${citation.authors}. ${citation.title}. ${citation.journal}. ${citation.year}`;
  if (citation.volume) {
    formatted += `;${citation.volume}`;
  }
  if (citation.pages) {
    formatted += `:${citation.pages}`;
  }
  if (citation.doi) {
    formatted += `. doi:${citation.doi}`;
  }
  return formatted;
}

export function CitationsList({ citations }: CitationsListProps) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <BookOpen className="h-5 w-5 text-blue-600" />
          References
          <span className="ml-auto text-sm font-normal text-gray-500">
            {citations.length} sources
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ol className="space-y-3">
          {citations.map((citation, index) => (
            <li key={citation.id}>
              <div className="flex gap-3 text-sm">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-semibold text-blue-700">
                  {citation.id}
                </span>
                <div className="flex-1">
                  <p className="text-gray-700 leading-relaxed">
                    {formatAmaCitation(citation)}
                  </p>
                  {citation.doi && (
                    <a
                      href={`https://doi.org/${citation.doi}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-1 inline-flex items-center gap-1 text-xs text-blue-600 hover:underline"
                    >
                      <ExternalLink className="h-3 w-3" />
                      View source
                    </a>
                  )}
                  {citation.pmid && (
                    <a
                      href={`https://pubmed.ncbi.nlm.nih.gov/${citation.pmid}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-1 inline-flex items-center gap-1 text-xs text-blue-600 hover:underline"
                    >
                      <ExternalLink className="h-3 w-3" />
                      PubMed
                    </a>
                  )}
                </div>
              </div>
              {index < citations.length - 1 && (
                <Separator className="mt-3" />
              )}
            </li>
          ))}
        </ol>
      </CardContent>
    </Card>
  );
}
