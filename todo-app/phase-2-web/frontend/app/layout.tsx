import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "Todo App",
  description: "A secure todo application with authentication and task management",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`antialiased min-h-screen`}
      >
        <Navbar />
        <div className="container mx-auto px-4 py-6">
          {children}
        </div>
      </body>
    </html>
  );
}
