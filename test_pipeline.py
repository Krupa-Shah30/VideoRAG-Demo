#!/usr/bin/env python3

from final import run_pipeline
import os

def test_video_processing():
    video_filename = '05_CPUMemoryIO_sm.mp4'
    video_path = f'uploaded_videos/{video_filename}'
    
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return
    
    print(f"🎬 Processing video: {video_path}")
    try:
        result = run_pipeline(video_filename)
        print(f"✅ Pipeline result: {result}")
        return result
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_video_processing()
