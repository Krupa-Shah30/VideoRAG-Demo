import React, { useEffect, useState } from "react";

interface EmbeddedVideoSelectorProps {
  onSelect: (hash: string) => void;
  onUpload: (file: File) => void;
}

const EmbeddedVideoSelector: React.FC<EmbeddedVideoSelectorProps> = ({ onSelect, onUpload }) => {
  const [embeddedVideos, setEmbeddedVideos] = useState<Array<{ hash: string; filename: string }>>([]);
  const [selected, setSelected] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/check-embeddings")
      .then(res => res.json())
      .then(data => {
        if (data.exists && data.data) {
          // Try to get filename from metadata, fallback to hash
          const videos = Object.entries(data.data).map(([hash, meta]: any) => ({
            hash,
            filename: meta.filename || hash
          }));
          setEmbeddedVideos(videos);
        }
      });
  }, []);

  const handleDropdownChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelected(e.target.value);
    onSelect(e.target.value);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div>
      <label>Select an embedded video:</label>
      <select value={selected} onChange={handleDropdownChange}>
        <option value="">-- Select --</option>
        {embeddedVideos.map((vid) => (
          <option key={vid.hash} value={vid.hash}>
            {vid.filename}
          </option>
        ))}
      </select>
      <div className="my-2">or</div>
      <input type="file" accept="video/mp4" onChange={handleFileChange} />
    </div>
  );
};

export default EmbeddedVideoSelector;
