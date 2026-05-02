import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { Calendar, FileText } from 'lucide-react';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { SectionCard } from '@/components/SectionCard';
import { CitationsList } from '@/components/CitationsList';
import { PrintButton } from './PrintButton';
import { Handout } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

async function fetchHandout(slug: string): Promise<Handout | null> {
  try {
    const res = await fetch(`${API_URL}/api/handouts/${slug}`, {
      cache: 'no-store',
    });
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`API ${res.status}`);
    return (await res.json()) as Handout;
  } catch (err) {
    console.error('Failed to fetch handout', err);
    return null;
  }
}

export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> }
): Promise<Metadata> {
  const { slug } = await params;
  const handout = await fetchHandout(slug);
  if (!handout) return { title: 'Handout not found' };
  return {
    title: handout.title,
    description: `Patient recovery instructions — ${handout.title}`,
    openGraph: {
      title: handout.title,
      description: `Recovery instructions generated ${new Date(handout.generatedAt).toLocaleDateString()}`,
    },
  };
}

export default async function PatientHandoutPage(
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params;
  const handout = await fetchHandout(slug);
  if (!handout) notFound();

  const formattedDate = new Date(handout.generatedAt).toLocaleDateString(
    'en-US',
    { year: 'numeric', month: 'long', day: 'numeric' }
  );

  return (
    <div className="min-h-screen bg-gray-50 print:bg-white">
      <main className="container mx-auto max-w-3xl px-4 py-6 sm:py-10">
        <Card className="bg-gradient-to-r from-blue-600 to-blue-700 text-white print:bg-white print:text-black">
          <CardHeader>
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-start gap-3">
                <div className="rounded-lg bg-white/10 p-3 print:bg-blue-100">
                  <FileText className="h-7 w-7" />
                </div>
                <div>
                  <CardTitle className="text-xl font-bold sm:text-2xl">
                    {handout.title}
                  </CardTitle>
                  <div className="mt-1 flex items-center gap-2 text-sm text-blue-100 print:text-gray-600">
                    <Calendar className="h-4 w-4" />
                    <span>Generated {formattedDate}</span>
                  </div>
                </div>
              </div>
              <PrintButton />
            </div>
          </CardHeader>
        </Card>

        <div className="mt-6 space-y-4">
          {handout.sections.map((section, index) => (
            <SectionCard
              key={section.id}
              section={section}
              defaultOpen={index === 0}
            />
          ))}
        </div>

        <div className="mt-6">
          <CitationsList citations={handout.citations} />
        </div>

        <p className="mt-8 text-center text-xs text-gray-500 print:hidden">
          PostOpCare — evidence-based recovery instructions. Always follow your surgeon&apos;s specific guidance.
        </p>
      </main>
    </div>
  );
}
