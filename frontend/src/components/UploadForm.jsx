import { useState, useRef } from "react";
import axios from "axios";
import { Plus, Upload, Trash2, X, FileImage, FileVideo, FileAudio, FileText, FileIcon } from "lucide-react";

export default function FileUpload() {
  // files: list of files + progress info:
  const [files, setFiles] = useState([]);       
  const [uploading, setUploading] = useState(false);
  const inputRef = useRef(null);                

  function handleFileSelect(e) {
    if (!e.target.files.length) return;
    const newFiles = Array.from(e.target.files).map((file) => ({
      //the id : name + size to make files more unique and to avoid eliminating 2 different files with the same name 
      // in the filter function
      id: `${file.name}-${file.size}`,
      file,
      progress: 0,
      uploaded: false,
    }));
    setFiles((prev) => {
      const all= [...prev, ...newFiles];
      //we shouldn't just combine the 2 lists without removing replicates:
      //so we add a filter to remove the replicates of files basing on the name + the size (which is the id)"
      const unique = all.filter(
        (file, index, arr)=> index === arr.findIndex((f)=> f.id === file.id)
      )
      return unique

    }    
      );
    if (inputRef.current) inputRef.current.value = ""; 
  }

  
  async function handleUpload() {
    if (files.length === 0 || uploading) return;
    setUploading(true);

    const uploadPromises = files.map(async (f) => {
      const formData = new FormData();
      formData.append("files", f.file);

      try {
        await axios.post("postgres-chatbot-production-627a.up.railway.app/api/upload/", formData, {
          onUploadProgress: (progressEvent) => {
            const percent = Math.round(
              (progressEvent.loaded * 100) / (progressEvent.total || 1)
            );
            setFiles((prev) =>
              prev.map((file) =>
                file.id === f.id ? { ...file, progress: percent } : file
              )
            );
          },
        });

        setFiles((prev) =>
          prev.map((file) =>
            file.id === f.id ? { ...file, uploaded: true } : file
          )
        );
      } catch (err) {
        console.error(err);
      }
    });

    await Promise.all(uploadPromises);
    setUploading(false);
  }

  function removeFile(id) {
    setFiles((prev) => prev.filter((f) => f.id !== id));
  }

  function handleClear() {
    setFiles([]);
  }

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-bold">File Upload</h2>

      {/* Top buttons */}
      <div className="flex gap-2">
        <input
          ref={inputRef}
          type="file"
          multiple
          className="hidden"
          id="file-upload"
          onChange={handleFileSelect}
          disabled={uploading}
        />
        <label
          htmlFor="file-upload"
          className="flex cursor-pointer items-center gap-2 rounded-md bg-gray-700 px-6 py-2 text-white hover:opacity-90"
        >
          <Plus size={18} />
          Select Files
        </label>

        <button
          onClick={handleUpload}
          disabled={files.length === 0 || uploading}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-60"
        >
          <Upload size={18} />
          Upload
        </button>

        <button
          onClick={handleClear}
          disabled={files.length === 0 || uploading}
          className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 disabled:opacity-60"
        >
          <Trash2 size={18} />
          Clear All
        </button>
      </div>

      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-semibold">Files:</h3>
          {files.map((file) => (
            <div key={file.id} className="space-y-2 rounded-md bg-gray-100 p-4">
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-3">
                  {getFileIcon(file.file.type, 40)}
                  <div>
                    <p className="font-medium">{file.file.name}</p>
                    <p className="text-xs text-gray-600">
                      {formatFileSize(file.file.size)} • {file.file.type || "Unknown"}
                    </p>
                  </div>
                </div>
                {!uploading && (
                  <button onClick={() => removeFile(file.id)}>
                    <X size={16} className="text-gray-600" />
                  </button>
                )}
              </div>

              <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className={`h-full ${
                    file.uploaded ? "bg-green-500" : "bg-blue-500"
                  } transition-all`}
                  style={{ width: `${file.progress}%` }}
                />
              </div>
              <div className="text-xs text-right text-gray-500">
                {file.uploaded ? "Completed" : `${file.progress}%`}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function getFileIcon(mimeType, size = 24) {
  if (mimeType.startsWith("image/")) return <FileImage size={size} className="text-blue-500" />;
  if (mimeType.startsWith("video/")) return <FileVideo size={size} className="text-purple-500" />;
  if (mimeType.startsWith("audio/")) return <FileAudio size={size} className="text-pink-500" />;
  if (mimeType === "application/pdf") return <FileText size={size} className="text-red-500" />;
  return <FileIcon size={size} className="text-gray-500" />;
}

function formatFileSize(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}
