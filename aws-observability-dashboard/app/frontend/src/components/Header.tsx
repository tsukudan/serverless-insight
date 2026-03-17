"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Navigation from "./Navigation";

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-xl font-bold text-gray-900">
            Serverless Insight
          </Link>
          <Navigation />
        </div>
      </div>
    </header>
  );
}
