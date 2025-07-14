from fastapi import APIRouter, HTTPException,status, Depends,Header
from pydantic import BaseModel
from typing import List, Any, Optional
from final import run_pipeline
from llm_calling import final_pipeline
from dotenv import load_dotenv
import os
import cv2
from fastapi import FastAPI
from fastapi import UploadFile, File, BackgroundTasks
from pathlib import Path
import json



load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv("API_KEY")


router = APIRouter()

# --- Request Schemas ---
class ExtractRequest(BaseModel):
    videoPath: str
#     #outputPath: str

class QueryRequest(BaseModel):
    query: str
    video_hash: str | None = None  # Add video_hash as optional
    



def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

UPLOADS_DIR = Path("uploaded_videos")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# --- Endpoints ---
@router.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    print("Troubleshoot")
    # Defensive: file.filename can be None if not provided by client
    if not file.filename or not file.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only .mp4 videos are supported.")

    save_path = UPLOADS_DIR / file.filename

    if save_path.exists():
        # Check if already embedded using hash as key, fallback to filename
        embeddings_path = Path("embeddings.json")
        is_embedded = False
        if embeddings_path.exists():
            import json
            from final import get_video_hash
            with open(embeddings_path, "r", encoding="utf-8") as f:
                embeddings = json.load(f)
            video_hash = get_video_hash(save_path)
            print(f"DEBUG: video_hash for file {file.filename} is {video_hash}")
            print(f"DEBUG: embeddings.json keys: {list(embeddings.keys())}")
            if video_hash in embeddings or file.filename in embeddings:
                is_embedded = True
        if is_embedded:
            return {"status": "Already uploaded & embedded", "file": file.filename}
        else:
            raise HTTPException(status_code=409, detail=f"File '{file.filename}' already exists.")

    try:
        with open(save_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)

    except Exception as e:
        if save_path.exists():
            save_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

    # 🔑 Now run your SAME pipeline, async:
    background_tasks.add_task(run_pipeline, file.filename)

    return {"status": "Uploaded & processing started", "file": file.filename}

@router.get("/video-summary/{video_filename}")
async def get_video_summary(video_filename: str):
    summary_path = Path("Output_Videos/Transcript") / f"{video_filename}_summary.txt"
    if summary_path.exists():
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = f.read()
        return {"summary": summary}
    else:
        return {"summary": "Summary not available yet. Please try again later."}


@router.post("/query")
async def query_vector_db(request: QueryRequest):
    print("Received /query request:", request)
    query = request.query
    video_hash = request.video_hash

    print("➡️ /query calling final_pipeline...")
    final_output = final_pipeline(query, video_hash=video_hash)
    print("✅ final_pipeline output:", final_output)
    return final_output



@router.get("/check-embeddings")
async def check_embeddings_file():
    embeddings_path = Path("embeddings.json")
    if embeddings_path.exists():
        import json
        with open(embeddings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"exists": True, "data": data}
    else:
        return {"exists": False, "data": None}


@router.get("/embedded-videos")
async def get_embedded_videos():
    record_file = Path("embedded_videos.json")
    if record_file.exists():
        with open(record_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Return list of dicts with hash and filename
        return {"videos": [{"hash": h, "filename": fn} for h, fn in data.items()]}
    else:
        return {"videos": []}



