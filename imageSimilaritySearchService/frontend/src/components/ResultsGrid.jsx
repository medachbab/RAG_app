const BASE_URL = import.meta.env.VITE_HOME_URL || ""; 

export default function ResultsGrid({ results }) {
  const handleClick = (productId) => {
    window.location.href = `${BASE_URL}/product/${productId}`;
  };

  return (
    <div className="mt-10">
      <h2 className="text-xl font-semibold mb-4">Results</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {results.map((r, idx) => (
          <div
            key={idx}
            className="bg-white rounded-xl p-4 border border-gray-200 hover:shadow-lg transform hover:scale-[1.02] transition cursor-pointer"
            onClick={() => handleClick(r.product_id)}
          >
            <img
              src={r.image}
              alt={r.title || "Result"}
              className="w-full h-40 object-cover rounded-lg mb-3"
              onError={(e) => (e.target.style.display = "none")}
            />
            <p className="font-semibold text-gray-800">{r.title || "Untitled Product"}</p>
            <p className="text-sm text-gray-600 break-all">{r.product_id}</p>
            <p className="text-sm mt-2 text-gray-800">
              Similarity: <span className="font-semibold text-blue-600">{r.similarity}</span>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
