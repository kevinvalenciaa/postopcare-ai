// Specialty categories for procedures
export type Specialty = 'Orthopedic' | 'General Surgery' | 'OB/GYN' | 'Emergency';

// Individual procedure
export interface Procedure {
  id: string;
  name: string;
  specialty: Specialty;
  description?: string;
}

// Section types for handouts
export type SectionType =
  | 'overview'
  | 'pain-management'
  | 'activity-restrictions'
  | 'wound-care'
  | 'warning-signs'
  | 'follow-up-care';

// Citation in AMA format
export interface Citation {
  id: number;
  authors: string;
  title: string;
  journal: string;
  year: number;
  volume?: string;
  pages?: string;
  doi?: string;
  pmid?: string;
}

// Section content with citations
export interface HandoutSection {
  id: string;
  type: SectionType;
  title: string;
  content: string; // HTML content with citation superscripts
  citationIds: number[];
}

// Quality metrics for generated handout
export interface QualityMetrics {
  overallScore: number; // 0-100
  readabilityGrade: number; // e.g., 7.2 for 7th grade level
  citationCoverage: number; // percentage 0-100
  completeness: number; // percentage 0-100
  safetyCheck: 'passed' | 'flagged';
}

// Complete handout
export interface Handout {
  id: string;
  procedure: string;
  procedureCode?: string;
  generatedAt: string;
  title: string;
  sections: HandoutSection[];
  citations: Citation[];
  qualityMetrics: QualityMetrics;
  slug?: string;
  publicUrl?: string;
  qrUrl?: string;
}

// Generation progress step
export interface GenerationStep {
  id: string;
  label: string;
  status: 'pending' | 'in-progress' | 'completed';
}

// Progress steps for generation simulation
export const GENERATION_STEPS: Omit<GenerationStep, 'status'>[] = [
  { id: 'retrieve', label: 'Retrieving medical literature...' },
  { id: 'analyze', label: 'Analyzing clinical guidelines...' },
  { id: 'generate', label: 'Generating patient-friendly content...' },
  { id: 'citations', label: 'Adding citations and formatting...' },
  { id: 'validate', label: 'Validating quality metrics...' },
];
