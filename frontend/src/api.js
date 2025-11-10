import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const uploadFile = async (file, onProgress) => {
  const url = `${API_BASE}/api/upload/`;
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(url, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(percent);
      }
    },
  });
  return response.data;
};

export const ragQuery = async (query, top_k = 3) => {
  const url = `${API_BASE}/api/query/`;
  const response = await axios.post(url, { query, top_k }, {
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.data;
};
