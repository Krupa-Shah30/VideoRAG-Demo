from fastapi import APIRouter, HTTPException,status, Depends,Header
from pydantic import BaseModel
from typing import List, Any, Optional
from final import run_pipeline
from llm_calling import final_pipeline
from dotenv import load_dotenv
import os
import cv2
from fastapi import FastAPI



load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv("API_KEY")


router = APIRouter()

# --- Request Schemas ---
class ExtractRequest(BaseModel):
    videoPath: str
#     #outputPath: str

class QueryRequest(BaseModel):
    query: str
    



def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

# --- Endpoints ---
@router.post("/process")
async def input_processing(request: ExtractRequest):
    try:
        print("Processing started")
        qdrant, embedder = run_pipeline(request.videoPath)
        return {"message": "Processing complete"}
    except Exception as e:
        print("🔥 Error in processing:", str(e))
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/query")
async def query_vector_db(request: QueryRequest):
    # Implement your logic here
    query = request.query
    # Assuming you have a Qdrant client and embedder model initialized  
    final_output = final_pipeline(query) 
    # print("output shown")
    return final_output



