'use client';

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { proceduresBySpecialty, specialtyOrder } from '@/data/procedures';
import { hasHandoutForProcedure } from '@/data/mockHandouts';
import { Badge } from '@/components/ui/badge';

interface ProcedureSelectProps {
  value: string | null;
  onValueChange: (value: string) => void;
  disabled?: boolean;
}

export function ProcedureSelect({
  value,
  onValueChange,
  disabled = false,
}: ProcedureSelectProps) {
  return (
    <Select
      value={value || undefined}
      onValueChange={onValueChange}
      disabled={disabled}
    >
      <SelectTrigger className="w-full sm:w-[350px]">
        <SelectValue placeholder="Select a procedure..." />
      </SelectTrigger>
      <SelectContent>
        {specialtyOrder.map((specialty) => {
          const procedures = proceduresBySpecialty[specialty] || [];
          if (procedures.length === 0) return null;

          return (
            <SelectGroup key={specialty}>
              <SelectLabel className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                {specialty}
              </SelectLabel>
              {procedures.map((procedure) => {
                const hasHandout = hasHandoutForProcedure(procedure.id);
                return (
                  <SelectItem
                    key={procedure.id}
                    value={procedure.id}
                    className="py-2"
                  >
                    <div className="flex items-center gap-2">
                      <span>{procedure.name}</span>
                      {hasHandout && (
                        <Badge
                          variant="secondary"
                          className="text-[10px] px-1.5 py-0 bg-green-100 text-green-700"
                        >
                          Demo
                        </Badge>
                      )}
                    </div>
                  </SelectItem>
                );
              })}
            </SelectGroup>
          );
        })}
      </SelectContent>
    </Select>
  );
}
