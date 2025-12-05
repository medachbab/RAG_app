import React from "react";
import UploadForm from "./components/UploadForm";
import QueryForm from "./components/QueryForm";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-start justify-center py-8">
      <div className="w-full max-w-4xl space-y-6 px-4">
        <header className="text-center">
          <h1 className="text-2xl font-bold">products chatbot</h1>
          <p className="text-sm text-gray-600">ask any question about our products here</p>
        </header>
        <QueryForm />

        
      </div>
    </div>
  );
}
