const BACKEND_URL = import.meta.env.VITE_BACKEND_URL_image || "http://localhost:8000";

export async function searchImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BACKEND_URL}/search?k=7`, {
    method: "POST",
    body: formData,
  });

  return res.json();
}
