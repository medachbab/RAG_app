const BACKEND_URL = import.meta.env.VITE_BACKEND_URL_image || "http://159.89.9.71:8001";

export async function searchImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BACKEND_URL}/search?k=7`, {
    method: "POST",
    body: formData,
  });

  return res.json();
}
