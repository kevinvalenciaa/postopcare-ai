'use client';

import { Printer } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function PrintButton() {
  return (
    <Button
      variant="secondary"
      size="sm"
      onClick={() => window.print()}
      className="bg-white/10 text-white hover:bg-white/20 print:hidden"
    >
      <Printer className="mr-2 h-4 w-4" />
      Print
    </Button>
  );
}
