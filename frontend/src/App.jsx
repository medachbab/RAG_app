import React from "react";
import Navbar from "./components/Navbar";
import QueryForm from "./components/QueryForm";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-white text-gray-800">
      
      <Navbar />

      <div className="relative z-10 container mx-auto px-4 pt-24 pb-8 max-w-6xl">
        {/* Header */}
        <header className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-4">
            <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight">
              Products Chatbot
            </h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Ask questions about any product in our store and get responses with verified sources
          </p>
        </header>

        <div className="flex flex-col lg:flex-row gap-8">
          <div className="w-full">
            <div className="bg-white/80 backdrop-blur-lg rounded-2xl border border-gray-200 shadow-xl overflow-hidden">
              <QueryForm />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}