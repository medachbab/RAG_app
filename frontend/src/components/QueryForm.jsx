import React, { useState } from "react";
import { ragQuery } from "../api";

export default function QueryForm() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(3);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      setError("Please enter a question.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await ragQuery(query, parseInt(topK || 3));
      setResult(res);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || err.message || "Query failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-xl p-4 space-y-3">
      <h3 className="text-lg font-semibold">Ask a question about a product</h3>

      <form onSubmit={handleSubmit} className="space-y-2">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something about our products..."
          rows={3}
          className="w-full rounded-md border-gray-200 focus:ring-2 focus:ring-blue-200 p-2"
        />

        <div className="flex items-center gap-2">
          <label className="text-sm">Top K</label>
          <input
            type="number"
            min={1}
            max={10}
            value={topK}
            onChange={(e) => setTopK(e.target.value)}
            className="w-20 rounded-md border-gray-200 p-1"
          />
          <button
            className="ml-auto px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-60"
            type="submit"
            disabled={loading}
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
      </form>

      {error && <p className="text-red-600 text-sm">{error}</p>}

      {result && (
        <div className="pt-3 space-y-3">
          {/* --- Answer Card --- */}
          <div className="p-4 bg-green-50 rounded-lg border border-green-200">
            <h4 className="font-semibold text-green-800 mb-2">Answer</h4>
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
              {result.answer}
            </p>
          </div>

          {/* --- Sources --- */}
          {result.sources && (
            <div>
              <h4 className="font-semibold mb-2 text-gray-800">Sources</h4>
              <div className="space-y-2">
                {result.sources.map((src, i) => (
                  <div
                    key={i}
                    className="p-3 bg-gray-50 border border-gray-200 rounded-lg"
                  >
                    <p className="text-xs text-gray-500 mb-1">
                      <strong>Distance:</strong>{" "}
                      {src.distance && !isNaN(src.distance)
                        ? src.distance.toFixed(4)
                        : "—"}
                    </p>
                    <p className="text-sm text-gray-800 whitespace-pre-wrap">
                      {src.source.text}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
