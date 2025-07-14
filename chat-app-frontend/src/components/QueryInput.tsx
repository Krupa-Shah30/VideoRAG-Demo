import React, { useState } from "react";

interface Props {
  videoUrl: string | null;
  setAnswer: (answer: any) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setAnswerTimestamp: (answerTimestamp: number | null) => void; // <-- changed to number
  videoHash?: string | null; // <-- add this
  videoFile?: File | null;   // <-- add this if needed
  disabled?: boolean; // <-- ensure this is present
}

const QueryInput: React.FC<Props> = ({
  videoUrl,
  setAnswer,
  setLoading,
  setError,
  setAnswerTimestamp,
  videoHash,
  disabled,
}) => {
  const [query, setQuery] = useState("");
  const [localLoading, setLocalLoading] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!videoUrl) {
      setLocalError("Please upload a video first.");
      return;
    }

    if (!query.trim()) {
      setLocalError("Please enter a question.");
      return;
    }

    setLoading(true);
    setLocalLoading(true);
    setLocalError(null);
    setError(null);
    setAnswer("");
    setAnswerTimestamp(null);

    try {
      // Pass videoHash to backend if available
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          video_hash: videoHash, // <-- pass hash
        }),
      });

      if (!response.ok) {
        throw new Error("API error video not uploaded");
      }

      const data = await response.json();
      if (!data.synthesized_answer) {
        throw new Error("No answer found for the given question.");
      }
      setAnswer(data.synthesized_answer);
      setAnswerTimestamp(data.start_timestamp);

      // Scroll to answer box
      setTimeout(() => {
        const answerBox = document.getElementById("answer-box");
        if (answerBox) {
          const yOffset = -80;
          const y = answerBox.getBoundingClientRect().top + window.pageYOffset + yOffset;
          window.scrollTo({ top: y, behavior: "smooth" });
        }
      }, 100);
    } catch (err) {
      console.error("API error:", err);
      setLocalError("Something went wrong. Please try again.");
      setError("Something went wrong. Please try again.");
      setAnswerTimestamp(null);
    } finally {
      setLoading(false);
      setLocalLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <div className="my-4 max-w-xl mx-auto flex items-center gap-4">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question"
        className="border-4 border-[#140C64] px-4 py-3 rounded-l-lg text-lg flex-1 focus:outline-none focus:ring-2 focus:ring-blue-300 shadow-sm"
        disabled={localLoading || disabled}
        style={{ minWidth: '250px' }}
      />
      <button
        onClick={handleSubmit}
        disabled={localLoading || disabled}
        className={`px-6 py-3 rounded-r-lg text-2xl font-extrabold transition-colors duration-200 shadow-sm ${
          localLoading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-[#ee2d3d] hover:bg-[#d72631] text-white"
        }`}
        style={{ minWidth: '140px' }}
      >
        {localLoading ? "Searching..." : "Search"}
      </button>
      {localError && <p className="text-red-600 mt-2 text-sm w-full">{localError}</p>}
    </div>
  );
};

export default QueryInput;
