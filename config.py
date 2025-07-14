from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env into the environment

# Qdrant settings
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "multimodal_video_data")

# Embedding & transcription models
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "clip-ViT-L-14")
TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL", "base")

# Frame extraction
FRAME_RATE = int(os.getenv("FRAME_RATE", 2))

# Text chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 200))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

# Embedding dimensionality
VECTOR_DIM = int(os.getenv("VECTOR_DIM", 768))


MIN_SCORE = 0.1
