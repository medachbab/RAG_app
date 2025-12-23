import React from "react";
import QueryForm from "./components/QueryForm";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-gray-100">

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-4">
            <h1 className="text-4xl md:text-5xl font-bold">
              Product Chatbot
            </h1>
          </div>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            Ask questions about any product in our store and get responses with verified sources
          </p>
        </header>

        {/* Main Chat Interface */}
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="w-full">
            <div className="bg-gradient-to-br from-gray-800/70 to-gray-900/70 backdrop-blur-lg rounded-2xl border border-gray-700/50 shadow-2xl overflow-hidden">
              <QueryForm />
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>Ask your questions about any product in our store</p>
        </footer>
      </div>
    </div>
  );
}