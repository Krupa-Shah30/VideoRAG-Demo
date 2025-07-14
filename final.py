from frame_extractor import FrameExtractor
from audio_extractor import AudioExtractor
from transcriber import AudioTranscriber
from embedder import EmbeddingProcessor
from qdrant_handler import QdrantHandler
from text_image_indexer import TextImageIndexer
from pathlib import Path
import config
import hashlib
import json
from summarizer import summarize_text

def get_video_hash(video_path):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(video_path, 'rb') as f:
        while chunk := f.read(BUF_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def is_video_processed(hash_str, record_file='embedded_videos.json'):
    record = Path(record_file)
    if record.exists():
        processed = json.loads(record.read_text())
    else:
        processed = {}
    return hash_str in processed

def mark_video_processed(hash_str, filename, record_file='embedded_videos.json'):
    record = Path(record_file)
    if record.exists():
        processed = json.loads(record.read_text())
    else:
        processed = {}
    processed[hash_str] = filename
    record.write_text(json.dumps(processed, indent=2))

def run_pipeline(video_file):
    uploads_dir = Path("uploaded_videos")
    video_path = uploads_dir / video_file

    video_hash = get_video_hash(video_path)
    print("Hash Created")
    print(f"DEBUG: video_hash used for upload: {video_hash}")

    if is_video_processed(video_hash):
        print("⚠️ Video already processed. Skipping embedding and upload.")
        qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)
        embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)
        return qdrant, embedder

    if video_path.is_file() and video_path.suffix.lower() == ".mp4":
        print(f"\n▶️ Running pipeline for: {video_path}")
    else:
        raise ValueError(f"❌ Invalid input path. Expected a single .mp4 file. Got: {video_path}")

    # ✅ Use Path for outputs too
    working_dir = Path("Output_Videos")
    frame_dir = working_dir / "Frames"
    audio_dir = working_dir / "Audio"
    transcript_dir = working_dir / "Transcript"

    print("📼 Extracting frames...")
    FrameExtractor(config.FRAME_RATE).extract_frames(video_path, str(frame_dir))

    print("🔊 Extracting audio...")
    AudioExtractor().extract_audio(video_path, str(audio_dir))

    print("📝 Transcribing audio...")
    # Find the specific MP3 file for this video
    expected_audio_name = video_path.stem + ".mp3"
    audio_path = audio_dir / expected_audio_name
    
    if not audio_path.exists():
        raise FileNotFoundError(f"Expected audio file {audio_path} not found")
    
    AudioTranscriber(config.TRANSCRIPTION_MODEL).transcribe(str(audio_path), str(transcript_dir))

    # --- Summarize transcript ---
    # Use the transcript file that matches the current video
    transcript_path = transcript_dir / f"{video_path.stem}_timestamped.txt"
    if transcript_path.exists():
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = f.read()
        print("Transcript being summarized:")
        print(transcript)
        print("📝 Summarizing transcript...")
        summary = summarize_text(transcript)
        print(f"Video summary: {summary}")
        # Optionally save summary
        with open(transcript_dir / f"{video_file}_summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
    else:
        summary = "No transcript found to summarize."

    print("📊 Generating embeddings...")
    embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)
    indexer = TextImageIndexer(embedder, config.CHUNK_SIZE, config.CHUNK_OVERLAP, video_hash=video_hash)
    text_nodes = indexer.index_text(str(transcript_dir))
    image_nodes = indexer.index_images(str(frame_dir))

    # --- DEBUG: Print transcript and embedding info ---
    print(f"Transcript directory: {transcript_dir}")
    for fname in Path(transcript_dir).glob("*.txt"):
        print(f"Transcript file: {fname}")
        with open(fname, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"First 5 lines of transcript: {lines[:5]}")
    print(f"Number of text embedding nodes: {len(text_nodes)}")
    print(f"Number of image embedding nodes: {len(image_nodes)}")
    # --- END DEBUG ---

    print("🧠 Uploading embeddings to Qdrant...")
    qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)
    qdrant.upload(text_nodes + image_nodes)

    mark_video_processed(video_hash, video_file)
    print("✅ All data uploaded to Qdrant!")
    return qdrant, embedder, summary
