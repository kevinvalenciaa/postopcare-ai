'use client';

import { Stethoscope, Sparkles } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export function Header() {
  return (
    <header className="border-b bg-white">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
              <Stethoscope className="h-6 w-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold text-gray-900">PostopCare</h1>
                <Badge variant="secondary" className="text-xs">
                  <Sparkles className="mr-1 h-3 w-3" />
                  AI-Powered
                </Badge>
              </div>
              <p className="text-sm text-gray-600">
                Evidence-based post-operative patient instructions
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
