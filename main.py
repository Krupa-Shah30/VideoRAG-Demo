from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apiRoutes import router
import uvicorn
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the directory exists
os.makedirs("uploaded_videos", exist_ok=True)
# Mount the uploaded_videos directory for static file serving
app.mount("/uploaded_videos", StaticFiles(directory="uploaded_videos"), name="uploaded_videos")

app.include_router(router)

if __name__ == "__main__":                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
