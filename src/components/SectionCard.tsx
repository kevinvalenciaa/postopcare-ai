'use client';

import { useState } from 'react';
import {
  ChevronDown,
  ClipboardList,
  Pill,
  Activity,
  Bandage,
  AlertTriangle,
  Calendar,
  LucideIcon,
} from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { HandoutSection, SectionType } from '@/types';
import { cn } from '@/lib/utils';

interface SectionCardProps {
  section: HandoutSection;
  defaultOpen?: boolean;
  onCitationClick?: (citationId: number) => void;
}

const sectionIcons: Record<SectionType, LucideIcon> = {
  overview: ClipboardList,
  'pain-management': Pill,
  'activity-restrictions': Activity,
  'wound-care': Bandage,
  'warning-signs': AlertTriangle,
  'follow-up-care': Calendar,
};

const sectionColors: Record<SectionType, string> = {
  overview: 'text-blue-600 bg-blue-50',
  'pain-management': 'text-purple-600 bg-purple-50',
  'activity-restrictions': 'text-orange-600 bg-orange-50',
  'wound-care': 'text-teal-600 bg-teal-50',
  'warning-signs': 'text-red-600 bg-red-50',
  'follow-up-care': 'text-green-600 bg-green-50',
};

export function SectionCard({
  section,
  defaultOpen = true,
  onCitationClick,
}: SectionCardProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const Icon = sectionIcons[section.type] || ClipboardList;
  const colorClass = sectionColors[section.type] || 'text-gray-600 bg-gray-50';

  return (
    <Card className="overflow-hidden">
      <Collapsible open={isOpen} onOpenChange={setIsOpen}>
        <CollapsibleTrigger asChild>
          <CardHeader className="cursor-pointer select-none hover:bg-gray-50 transition-colors">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className={cn('rounded-lg p-2', colorClass)}>
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {section.title}
                </h3>
              </div>
              <ChevronDown
                className={cn(
                  'h-5 w-5 text-gray-400 transition-transform duration-200',
                  isOpen && 'rotate-180'
                )}
              />
            </div>
          </CardHeader>
        </CollapsibleTrigger>
        <CollapsibleContent>
          <CardContent className="pt-0">
            <div
              className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-h4:text-base prose-h4:font-semibold prose-h4:mt-4 prose-h4:mb-2 prose-p:text-gray-700 prose-li:text-gray-700 prose-strong:text-gray-900 prose-ul:my-2 prose-li:my-0.5"
              dangerouslySetInnerHTML={{ __html: section.content }}
            />
            {section.citationIds.length > 0 && (
              <div className="mt-4 flex flex-wrap items-center gap-1 text-xs text-gray-500">
                <span>References:</span>
                {section.citationIds.map((id, index) => (
                  <button
                    key={id}
                    onClick={() => onCitationClick?.(id)}
                    className="rounded bg-blue-100 px-1.5 py-0.5 text-blue-700 hover:bg-blue-200 transition-colors"
                  >
                    [{id}]
                  </button>
                ))}
              </div>
            )}
          </CardContent>
        </CollapsibleContent>
      </Collapsible>
    </Card>
  );
}
