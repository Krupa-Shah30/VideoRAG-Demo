from frame_extractor import FrameExtractor
from audio_extractor import AudioExtractor
from transcriber import AudioTranscriber
from embedder import EmbeddingProcessor
from qdrant_handler import QdrantHandler
from text_image_indexer import TextImageIndexer
import os
import config
import hashlib
import json
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




def get_video_hash(video_path):

    # video_path = os.path.join(v_path, videopath)
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(video_path, 'rb') as f:
        while chunk := f.read(BUF_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def is_video_processed(hash_str, record_file='embedded_videos.json'):
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            processed = json.load(f)
    else:
        processed = {}
    return hash_str in processed

def mark_video_processed(hash_str, record_file='embedded_videos.json'):
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            processed = json.load(f)
    else:
        processed = {}

    processed[hash_str] = "embedded"

    with open(record_file, 'w') as f:
        json.dump(processed, f, indent=2)

def run_pipeline(video_file):
    print(video_file)
    video_file = video_file.replace(":", "_")
    directory = r"C:/Users/Yash S/Documents/vrag_videos"
    video_path = os.path.join(directory,video_file)
# def run_pipeline():
#     video_path=r"C:/Users/Yash S/Documents/vrag_videos/WhatMakesAComputer.mp4"

    # print(video_path)
    video_hash = get_video_hash(video_path)
    print("Hash Created")
    if is_video_processed(video_hash):
        print("⚠️ Video already processed. Skipping embedding and upload.")
        qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)
        embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)
        return qdrant, embedder
    
    if os.path.isfile(video_path) and video_path.lower().endswith(".mp4"):
        print(f"\n▶️ Running pipeline for single video file: {video_path}")
    else:
        raise ValueError(f"❌ Invalid input path. Expected direct path to a single .mp4 file. Got: {video_path}")



    # Create output dirs
    working_dir=r"C:/Users/Yash S/Documents/Output_Videos"
    frame_dir = os.path.join(working_dir, "Frames")
    audio_dir = os.path.join(working_dir, "Audio")
    transcript_dir = os.path.join(working_dir, "Transcript")

    print("📼 Extracting frames...")
    FrameExtractor(config.FRAME_RATE).extract_frames(video_path, frame_dir)

    print("🔊 Extracting audio...")
    AudioExtractor().extract_audio(video_path, audio_dir)

    print("📝 Transcribing audio...")
    mp3_files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]
    if not mp3_files:
        raise FileNotFoundError(f"No .mp3 file found in {audio_dir}")
    audio_path = os.path.join(audio_dir, mp3_files[0])

    AudioTranscriber(config.TRANSCRIPTION_MODEL).transcribe(audio_path, transcript_dir)

    print("📊 Generating embeddings...")
    embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)
    indexer = TextImageIndexer(embedder, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    text_nodes = indexer.index_text(transcript_dir)
    image_nodes = indexer.index_images(frame_dir)

    print("🧠 Uploading embeddings to Qdrant...")
    qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)
    qdrant.upload(text_nodes + image_nodes)

    mark_video_processed(video_hash)
    print("✅ All data uploaded to Qdrant!")
    return qdrant, embedder

# if __name__ == "__main__":
#     print(run_pipeline())
    
    
