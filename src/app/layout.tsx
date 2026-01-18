import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PostopCare - AI-Powered Post-Operative Instructions",
  description:
    "Generate evidence-based, citation-backed patient handouts for post-operative care in seconds.",
  keywords: [
    "post-operative care",
    "patient instructions",
    "surgery recovery",
    "medical handouts",
    "healthcare",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
