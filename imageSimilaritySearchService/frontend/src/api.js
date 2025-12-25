export async function searchImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://localhost:8000/search?k=5", {
    method: "POST",
    body: formData,
  });

  return res.json();
}
