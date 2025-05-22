"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";

interface SignInModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const SignInModal: React.FC<SignInModalProps> = ({ isOpen, onClose }) => {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="relative bg-white rounded-2xl shadow-xl px-10 py-8 w-full max-w-xl">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-6 text-2xl font-semibold text-gray-500 hover:text-[#007698]"
        >
          &times;
        </button>

        {/* Title */}
        <h2 className="text-4xl font-bold text-[#005eb4] tracking-wide text-center mb-2">
          Welcome! 👋
        </h2>
        <p className="text-lg text-gray-700 text-center mb-6 tracking-wide">
          Let’s create your account
        </p>

        {/* Inputs */}
        <div className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#007698]"
          />
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#007698]"
          />
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#007698]"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#007698]"
          />
        </div>

        {/* Buttons */}
        <div className="mt-6 space-y-3">
          <button
            onClick={() => {
              if (name.trim()) {
                localStorage.setItem("ecliptica_username", name.trim());
              }
              onClose();
              router.push("/dashboard");
            }}
            className="w-full bg-[#007698] text-white py-3 rounded-full text-lg font-medium hover:bg-blue-700 transition"
          >
            Create your account
          </button>
          <button className="w-full border border-gray-300 py-3 rounded-full text-lg hover:border-[#007698] transition">
            Sign in with Google
          </button>
          <button className="w-full border border-gray-300 py-3 rounded-full text-lg hover:border-[#007698] transition">
            Log in with GitHub
          </button>
        </div>
      </div>
    </div>
  );
};

export default SignInModal;
