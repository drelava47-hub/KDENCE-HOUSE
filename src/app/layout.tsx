import type { Metadata } from "next";
import "./globals.css";
import { env } from "@/env";

export const metadata: Metadata = {
  title: "KDENCE HOUSE Operations",
  description: "KDENCE HOUSE Operations application skeleton",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  void env;

  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
