import { useState } from "react";
import { searchImage } from "./api";
import Navbar from "./components/Navbar";

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
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
        
        {/* Header */}
        <h1 className="text-3xl font-bold text-center mb-2 text-gray-900">
        Image Similarity Search
        </h1>
        <p className="text-center text-gray-600 mb-8">
          Upload an image and find visually similar results
        </p>

        {/* Upload */}
        <div className="flex flex-col items-center gap-4">
          <label className="w-full max-w-md cursor-pointer border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-blue-500 transition">
            <input
              type="file"
              className="hidden"
              accept="image/*"
              onChange={handleFileChange}
            />
            <p className="text-gray-600">
              Click to upload or drag & drop an image
            </p>
          </label>

          {preview && (
            <img
              src={preview}
              alt="Preview"
              className="w-40 h-40 object-cover rounded-xl border border-gray-200"
            />
          )}

          <button
            onClick={handleSearch}
            disabled={!file || loading}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white rounded-xl font-semibold transition"
          >
            {loading ? "Searching..." : "Search"}
          </button>

          {error && (
            <p className="text-red-600 mt-2">{error}</p>
          )}
        </div>

        {/* Results */}
        {results.length > 0 && (
          <div className="mt-10">
            <h2 className="text-xl font-semibold mb-4">
              Results
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {results.map((r, idx) => (
                <div
                  key={idx}
                  className="bg-white rounded-xl p-4 border border-gray-200 hover:shadow-lg transform hover:scale-[1.02] transition"
                >
                  <img
                    src={r.image}
                    alt="Result"
                    className="w-full h-40 object-cover rounded-lg mb-3"
                    onError={(e) => {
                      e.target.style.display = "none";
                    }}
                  />
                  <p className="text-sm text-gray-600 break-all">
                    {r.image}
                  </p>
                  <p className="text-sm mt-2 text-gray-800">
                    Similarity:{" "}
                    <span className="font-semibold text-blue-600">
                      {r.similarity}
                    </span>
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  </div>
  );
}
