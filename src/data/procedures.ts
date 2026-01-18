import { Procedure, Specialty } from '@/types';

export const procedures: Procedure[] = [
  // Orthopedic
  {
    id: 'total-knee-replacement',
    name: 'Total Knee Replacement',
    specialty: 'Orthopedic',
    description: 'Total knee arthroplasty (TKA)',
  },
  {
    id: 'total-hip-replacement',
    name: 'Total Hip Replacement',
    specialty: 'Orthopedic',
    description: 'Total hip arthroplasty (THA)',
  },
  {
    id: 'acl-reconstruction',
    name: 'ACL Reconstruction',
    specialty: 'Orthopedic',
    description: 'Anterior cruciate ligament reconstruction',
  },

  // General Surgery
  {
    id: 'laparoscopic-cholecystectomy',
    name: 'Laparoscopic Cholecystectomy',
    specialty: 'General Surgery',
    description: 'Gallbladder removal surgery',
  },
  {
    id: 'laparoscopic-appendectomy',
    name: 'Laparoscopic Appendectomy',
    specialty: 'General Surgery',
    description: 'Appendix removal surgery',
  },
  {
    id: 'inguinal-hernia-repair',
    name: 'Inguinal Hernia Repair',
    specialty: 'General Surgery',
    description: 'Hernia repair surgery',
  },

  // OB/GYN
  {
    id: 'cesarean-section',
    name: 'Cesarean Section (C-Section)',
    specialty: 'OB/GYN',
    description: 'Surgical delivery of baby',
  },
  {
    id: 'laparoscopic-hysterectomy',
    name: 'Laparoscopic Hysterectomy',
    specialty: 'OB/GYN',
    description: 'Uterus removal surgery',
  },

  // Emergency
  {
    id: 'ankle-fracture',
    name: 'Ankle Fracture (Cast Care)',
    specialty: 'Emergency',
    description: 'Ankle fracture management',
  },
  {
    id: 'concussion',
    name: 'Concussion',
    specialty: 'Emergency',
    description: 'Mild traumatic brain injury care',
  },
];

// Group procedures by specialty
export const proceduresBySpecialty = procedures.reduce(
  (acc, procedure) => {
    if (!acc[procedure.specialty]) {
      acc[procedure.specialty] = [];
    }
    acc[procedure.specialty].push(procedure);
    return acc;
  },
  {} as Record<Specialty, Procedure[]>
);

// Get procedure by ID
export const getProcedureById = (id: string): Procedure | undefined => {
  return procedures.find((p) => p.id === id);
};

// Specialty order for display
export const specialtyOrder: Specialty[] = [
  'Orthopedic',
  'General Surgery',
  'OB/GYN',
  'Emergency',
];
