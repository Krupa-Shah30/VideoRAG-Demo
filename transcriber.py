# transcriber.py
'''
from faster_whisper import WhisperModel
import os

class AudioTranscriber:
    def __init__(self, model_name="base", device="cpu"):
        self.model = WhisperModel(model_name, device="cpu", compute_type="int8")

    def transcribe(self, audio_path, output_folder):  # ✅ accepts a file now
        os.makedirs(output_folder, exist_ok=True)
        print(f"🔊 Transcribing: {audio_path}")

        segments, _ = self.model.transcribe(audio_path)  #word_timestamps=True, language="en", beam_size=5)
        transcript_text = " ".join(segment.text.strip() for segment in segments)

        filename = os.path.basename(audio_path).replace(".mp3", "_plain.txt")
        transcript_path = os.path.join(output_folder, filename)

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        print(f"✅ Transcript saved: {transcript_path}")

'''
from faster_whisper import WhisperModel
import os
import re

class AudioTranscriber:
    def __init__(self, model_name="base", device="cpu"):
        self.model = WhisperModel(model_name, device=device, compute_type="int8")

    def split_into_sentences(self, text):
        """
        Splits text into sentences using simple regex.
        """
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s for s in sentences if s]

    def transcribe(self, audio_path, output_folder):
        """
        Transcribes audio and saves a timestamped transcript.
        """
        os.makedirs(output_folder, exist_ok=True)
        print(f"🔊 Transcribing: {audio_path}")

        segments, _ = self.model.transcribe(audio_path)

        transcript_lines = []
        for segment in segments:
            start_time = segment.start  # Start time of the segment in seconds
            sentences = self.split_into_sentences(segment.text)
            for sentence in sentences:
                timestamp = f"[{start_time:.2f}s]"
                transcript_lines.append(f"{timestamp} {sentence}")

        filename = os.path.basename(audio_path).replace(".mp3", "_timestamped.txt")
        transcript_path = os.path.join(output_folder, filename)

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write("\n".join(transcript_lines))

        print(f"✅ Timestamped transcript saved: {transcript_path}")
