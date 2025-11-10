import React from "react";
import UploadForm from "./components/UploadForm";
import QueryForm from "./components/QueryForm";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-start justify-center py-8">
      <div className="w-full max-w-4xl space-y-6 px-4">
        <header className="text-center">
          <h1 className="text-2xl font-bold">RAG Frontend</h1>
          <p className="text-sm text-gray-600">Upload documents, then ask questions about them.</p>
        </header>

        <UploadForm />
        <QueryForm />

        <footer className="text-center text-xs text-gray-500">
          Make sure your Django backend is running and CORS is configured.
        </footer>
      </div>
    </div>
  );
}
