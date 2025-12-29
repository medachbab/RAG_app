import { useState } from "react";
import { searchImage } from "./api";
import Navbar from "./components/Navbar";
import UploadForm from "./components/UploadForm";
import ResultsGrid from "./components/ResultsGrid";

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (selectedFile) => {
    if (!selectedFile) return;
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResults([]);
    setError(null);
  };

  const handleSearch = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    try {
      const data = await searchImage(file);
      setResults(data.results);
    } catch (err) {
      setError("Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-white text-gray-800">
      <Navbar />

      <div className="pt-24 flex items-center justify-center p-6">
        <div className="w-full max-w-4xl bg-white/90 backdrop-blur rounded-2xl shadow-xl p-8 border border-gray-200">
          <h1 className="text-3xl font-bold text-center mb-2 text-gray-900">
            Image Similarity Search
          </h1>
          <p className="text-center text-gray-600 mb-8">
            Upload an image and find visually similar results
          </p>

          <UploadForm
            preview={preview}
            onFileChange={handleFileChange}
            onSearch={handleSearch}
            loading={loading}
            error={error}
          />

          {results.length > 0 && <ResultsGrid results={results} />}
        </div>
      </div>
    </div>
  );
}
