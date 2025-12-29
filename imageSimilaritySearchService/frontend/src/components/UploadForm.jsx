export default function UploadForm({ preview, onFileChange, onSearch, loading, error }) {
  const handleChange = (e) => {
    const selected = e.target.files[0];
    onFileChange(selected);
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <label className="w-full max-w-md cursor-pointer border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-blue-500 transition">
        <input type="file" className="hidden" accept="image/*" onChange={handleChange} />
        <p className="text-gray-600">Click to upload or drag & drop an image</p>
      </label>

      {preview && (
        <img
          src={preview}
          alt="Preview"
          className="w-40 h-40 object-cover rounded-xl border border-gray-200"
        />
      )}

      <button
        onClick={onSearch}
        disabled={!preview || loading}
        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white rounded-xl font-semibold transition"
      >
        {loading ? "Searching..." : "Search"}
      </button>

      {error && <p className="text-red-600 mt-2">{error}</p>}
    </div>
  );
}
