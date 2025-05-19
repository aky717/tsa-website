"use client";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { usePathname } from "next/navigation";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const showNavbar = !pathname.startsWith("/dashboard");

  return (
    <html lang="en">
      <body>
        {showNavbar && <Navbar />}
        {children}
      </body>
    </html>
  );
}
