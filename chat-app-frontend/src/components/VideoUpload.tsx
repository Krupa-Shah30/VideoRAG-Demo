import React, { useState } from 'react';

interface Props {
  setVideoUrl: (url: string) => void;
  setError: (error: string | null) => void;
  setVideoHash: React.Dispatch<React.SetStateAction<string | null>>;
  setSelectedFile: React.Dispatch<React.SetStateAction<File | null>>;
  processing: boolean;
  setProcessing: React.Dispatch<React.SetStateAction<boolean>>;
  // Add a callback to trigger query UI
  onProceedToQuery?: (videoHash: string, file: File | null) => void;
  setUploadedFilename: React.Dispatch<React.SetStateAction<string | null>>; // <-- add this
}

const MAX_FILE_SIZE_MB = 100;

const VideoUpload: React.FC<Props> = ({ setVideoUrl, setError, setVideoHash, setSelectedFile, onProceedToQuery, setUploadedFilename }) => {
  const [loading, setLoading] = useState(false);
  const [uploadedFilename, setUploadedFilenameState] = useState<string | null>(null);
  const [isEmbedded, setIsEmbedded] = useState(false);
  const [videoHash, setVideoHashState] = useState<string | null>(null);
  const [selectedFile, setSelectedFileState] = useState<File | null>(null);

  // Compute SHA-256 hash of the file
  async function computeFileHash(file: File) {
    const arrayBuffer = await file.arrayBuffer();
    const hashBuffer = await window.crypto.subtle.digest("SHA-256", arrayBuffer);
    return Array.from(new Uint8Array(hashBuffer))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
  }

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setError(null);
    setLoading(true);
    setIsEmbedded(false);
    setUploadedFilenameState(null);
    setVideoHashState(null);
    setSelectedFileState(null);
    setSelectedFile(file);

    // Local preview for video player (keep!)
    const previewUrl = URL.createObjectURL(file);
    setVideoUrl(previewUrl);

    if (!file.type.startsWith("video/")) {
      setError("Please upload a valid video file.");
      setLoading(false);
      return;
    }

    const fileSizeMB = file.size / (1024 * 1024);
    if (fileSizeMB > MAX_FILE_SIZE_MB) {
      setError(`File size exceeds ${MAX_FILE_SIZE_MB}MB.`);
      setLoading(false);
      return;
    }

    try {
      // 1. Fetch embeddings.json from backend
      const res = await fetch("http://localhost:8000/check-embeddings");
      const { exists, data } = await res.json();
      const embeddings = exists ? data : {};

      // 2. Compute hash of the selected file
      const hash = await computeFileHash(file);
      console.log("Frontend computed video hash:", hash, "for file:", file.name); // <-- Add this line
      setVideoHashState(hash);
      setVideoHash(hash);

      // 3. Check if hash exists in embeddings
      if (embeddings[hash]) {
        setIsEmbedded(true);
        setUploadedFilenameState(file.name);
        setUploadedFilename(file.name); // <-- trigger parent update
        setError("Video already embedded. You can proceed to query.");
        setLoading(false);
        return;
      }

      // 4. Upload if not embedded
      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!uploadRes.ok) {
        const err = await uploadRes.json();
        throw new Error(err.detail || "Upload failed");
      }

      const uploadData = await uploadRes.json();
      setUploadedFilenameState(uploadData.file);
      setUploadedFilename(uploadData.file); // <-- trigger parent update
      setError(null);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  // Handler for "Proceed to Query" button
  const handleProceedToQuery = () => {
    if (onProceedToQuery && videoHash) {
      onProceedToQuery(videoHash, selectedFile);
    }
  };

  return (
    <div className="relative h-full">
      <label htmlFor="video-upload" className="block text-2xl font-semibold mt-0 mb-4">
        Upload a Video
      </label>
      <input
        id="video-upload"
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        className="block mb-0 bg-white rounded border p-2 cursor-pointer w-full"
        disabled={loading}
      />
      {uploadedFilename && (
        <div className="text-sm text-gray-700 mt-1">
          <strong>{isEmbedded ? "Already embedded:" : "Uploaded:"}</strong> {uploadedFilename}
        </div>
      )}
      {loading && <p className="text-blue-500 mt-1">Processing...</p>}

      {isEmbedded && (
        <button
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={handleProceedToQuery}
        >
          Proceed to Query
        </button>
      )}
    </div>
  );
};

export default VideoUpload;

