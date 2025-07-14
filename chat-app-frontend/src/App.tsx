import { useState, useRef, useEffect } from "react";
import VideoUpload from "./components/VideoUpload";
import QueryInput from "./components/QueryInput";
import AnswerDisplay from "./components/AnswerDisplay";
import { FaUpload, FaHistory, FaVideo } from "react-icons/fa";

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}

function App() {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [answer, setAnswer] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [answerTimestamp, setAnswerTimestamp] = useState<number | null>(null);
  const [videoHash, setVideoHash] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState<boolean>(false);
  const [uploadedFilename, setUploadedFilename] = useState<string | null>(null);
  const [summary, setSummary] = useState<string>("Upload a video to see its summary.");
  const [embeddedVideos, setEmbeddedVideos] = useState<{hash: string, filename: string}[]>([]);
  const [selectedHash, setSelectedHash] = useState<string>("");
  const [selectedFilename, setSelectedFilename] = useState<string>("");

  useEffect(() => {
    fetch("http://localhost:8000/embedded-videos")
      .then((res) => res.json())
      .then((data) => setEmbeddedVideos(data.videos || []));
  }, []);

  useEffect(() => {
    const filename = selectedFilename || uploadedFilename;
    if (!filename) return;
    fetch(`http://localhost:8000/video-summary/${filename}`)
      .then((res) => res.json())
      .then((data) => setSummary(data.summary))
      .catch(() => setSummary("Could not load summary."));
  }, [uploadedFilename, selectedFilename]);

  const previewVideoRef = useRef<HTMLVideoElement | null>(null);
  const answerVideoRef = useRef<HTMLVideoElement | null>(null);

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-100 font-sans">
      <header className="flex items-center justify-between px-8 py-4 bg-white shadow">
        <img src="/WL-image-1.webp" alt="App Logo" className="h-10" />
        <button className="bg-red-500 text-white px-5 py-2 rounded-lg font-bold shadow hover:bg-red-600 transition">New Chat</button>
      </header>
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-80 bg-white border-r shadow-lg flex flex-col gap-6 p-6">
          {/* Upload Section */}
          <div className="bg-gray-50 rounded-xl shadow p-4 flex flex-col gap-2">
            <div className="flex items-center gap-2 text-lg font-semibold">
              <FaUpload className="text-blue-500" /> Upload a Video
            </div>
            <VideoUpload
              setVideoUrl={(url) => {
                setVideoUrl(url);
                setAnswer("");
                setError(null);
                setAnswerTimestamp(null);
              }}
              setError={setError}
              setVideoHash={setVideoHash}
              setSelectedFile={setSelectedFile}
              processing={processing}
              setProcessing={setProcessing}
              setUploadedFilename={setUploadedFilename}
            />
          </div>
          {/* Summary Section */}
          <div className="bg-gray-50 rounded-xl shadow p-4 flex flex-col gap-2">
            <h4 className="font-bold text-gray-700 mb-1">Video Summary</h4>
            <div className="overflow-y-auto max-h-32 text-gray-600">{summary}</div>
          </div>
          {/* History Section */}
          <div className="bg-gray-50 rounded-xl shadow p-4 flex flex-col gap-2">
            <div className="flex items-center gap-2 text-lg font-semibold">
              <FaHistory className="text-purple-500" /> Upload History
            </div>
            <select
              className="w-full border rounded p-1 mb-2"
              value={selectedHash}
              onChange={e => {
                setSelectedHash(e.target.value);
                const found = embeddedVideos.find(v => v.hash === e.target.value);
                setSelectedFilename(found ? found.filename : "");
                setVideoHash(e.target.value);
                setUploadedFilename("");
                setVideoUrl(found ? `http://localhost:8000/uploaded_videos/${found.filename}` : null);
              }}
            >
              <option value="">Select embedded video</option>
              {embeddedVideos.map(v => (
                <option key={v.hash} value={v.hash}>{v.filename} ({v.hash.slice(0,8)}...)</option>
              ))}
            </select>
            <button className="bg-red-500 text-white px-3 py-1 rounded shadow hover:bg-red-600 transition">Clear history</button>
          </div>
        </aside>
        {/* Main Content */}
        <main className="flex-1 flex flex-col items-center justify-center p-10 bg-gradient-to-br from-white to-blue-100">
          <h2 className="text-3xl font-extrabold mb-4 text-gray-800">Ask a question</h2>
          {/* Video Display */}
          <div className="w-full max-w-3xl bg-white rounded-xl shadow-lg p-6 mb-6 flex flex-col items-center">
            <video
              src={videoUrl || (selectedFilename ? `http://localhost:8000/uploaded_videos/${selectedFilename}` : undefined)}
              controls
              className="w-full rounded-lg shadow"
            />
          </div>
          {/* Query Input */}
          <div className="w-full max-w-2xl flex gap-2 mb-6">
            <QueryInput
              videoUrl={videoUrl}
              setAnswer={setAnswer}
              setLoading={setLoading}
              setError={setError}
              setAnswerTimestamp={setAnswerTimestamp}
              videoHash={selectedHash || videoHash}
              videoFile={selectedFile}
              disabled={processing}
            />
          </div>
          <AnswerDisplay answer={answer} loading={loading} error={error} />
        </main>
        {/* Right Sidebar */}
        <aside className="w-80 bg-white border-l shadow-lg flex flex-col items-center p-6">
          <div className="bg-gray-50 rounded-xl shadow p-4 w-full flex flex-col items-center">
            <FaVideo className="text-2xl text-blue-400 mb-2" />
            <h3 className="text-lg font-semibold mb-2">Video Preview</h3>
            <video
              ref={previewVideoRef}
              src={videoUrl || (selectedFilename ? `http://localhost:8000/uploaded_videos/${selectedFilename}` : undefined)}
              muted
              playsInline
              className="w-full rounded shadow mb-2"
              onTimeUpdate={(e) => {
                if (e.currentTarget.currentTime > 10) {
                  e.currentTarget.pause();
                  e.currentTarget.currentTime = 0;
                }
              }}
            />
            <button
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition"
              onClick={() => {
                if (previewVideoRef.current) {
                  previewVideoRef.current.currentTime = 0;
                  previewVideoRef.current.play();
                }
              }}
            >
              Play
            </button>
            <p className="text-xs text-gray-500 mt-2 italic">Preview: first 10 seconds</p>
            {answerTimestamp !== null && (
              <>
                <h3 className="text-lg font-semibold mt-6 mb-2 text-center">
                  Answer Timestamp Preview
                </h3>
                <video
                  ref={answerVideoRef}
                  src={videoUrl || (selectedFilename ? `http://localhost:8000/uploaded_videos/${selectedFilename}` : undefined)}
                  muted
                  controls
                  className="w-full rounded shadow"
                  onLoadedMetadata={() => {
                    if (answerVideoRef.current) {
                      answerVideoRef.current.currentTime = answerTimestamp;
                      answerVideoRef.current.pause();
                    }
                  }}
                />
                <button
                  onClick={() => {
                    if (answerVideoRef.current) {
                      answerVideoRef.current.currentTime = answerTimestamp;
                      answerVideoRef.current.play();
                    }
                  }}
                  className="mt-2 px-3 py-1 bg-purple-600 text-white rounded hover:bg-purple-700 text-sm font-medium"
                >
                  Play from {formatTime(answerTimestamp)}
                </button>
                <p className="text-xs text-gray-500 mt-2 italic text-center">
                  Preview at {formatTime(answerTimestamp)}
                </p>
              </>
            )}
          </div>
        </aside>
      </div>
      <footer className="text-center py-4 text-gray-400 text-sm bg-white border-t">© 2024 WorldLink</footer>
    </div>
  );
}

export default App;
