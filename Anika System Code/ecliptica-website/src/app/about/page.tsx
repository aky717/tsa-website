'use client';

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import Hover from "@/components/ui/Hover";

export default function About() {
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/run_ctm', {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Server error');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'outputs.zip';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error:', err);
      alert('Something went wrong. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="overflow-x-hidden">
      {/* Background section */}
      <div
        className="relative w-full h-screen bg-cover bg-center"
        style={{ backgroundImage: "url(/imgs/background.jpg)" }}
      >
        <div className="absolute inset-0 flex flex-col items-center justify-center z-10">
          <h1 className="text-6xl text-center text-[#005eb4] leading-tight tracking-wider font-bold">
            Our Product <br />
          </h1>
          <p className="text-2xl text-black mt-4">
            Accessible expert research. Everywhere.
          </p>
        </div>
      </div>

      {/* CTA section */}
      <div className="w-full bg-[#d4ecff] py-20 text-center">
        <h2 className="text-[#005eb4] text-5xl font-semibold mb-10">
          Discover Something New.
        </h2>

        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-[#007698] text-white py-4 px-10 rounded-full text-lg font-medium hover:bg-blue-700 transition disabled:opacity-50"
        >
          Start Your Research Now
        </button>

        {/* Loading spinner */}
        {loading && (
          <div className="flex items-center justify-center mt-6">
            <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-blue-500 border-opacity-70"></div>
            <p className="ml-4 text-lg text-blue-800">Processing…</p>
          </div>
        )}
      </div>

      {/* Possible Data Visualizations Section */}
      <Hover />

      {/* Call-to-action section */}
      <div className="bg-[#99ceff] w-full">
        <div className="flex flex-col items-center justify-center relative space-y-10 py-20">
          <p className="text-5xl text-[#005eb4]">
            Let’s Research With the Click of a Button
          </p>
          <p className="text-2xl text-[#005eb4]">
            Compile a list of publications and data visualizations with just one keyword.
          </p>

          <Link href="#">
            <button className="text-center items-center justify-center center-20 relative bg-[#007698] text-white py-4 px-10 rounded-full text-lg font-medium mt-4 hover:bg-blue-700 transition">
              Explore More About Ecliptica &rarr;
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
