import cv2
import os
from datetime import timedelta
from collections import defaultdict

class FrameExtractor:
    def __init__(self, frame_rate=1):
        self.frame_rate = frame_rate

    def extract_frames(self, video_path, output_folder):
        # Ensure video_path is a string for os and string methods
        video_path_str = str(video_path)
        if not (os.path.isfile(video_path_str) and video_path_str.lower().endswith(".mp4")):
            raise ValueError(f"❌ Expected a single .mp4 file. Got: {video_path}")

        os.makedirs(output_folder, exist_ok=True)

        video_file = os.path.basename(video_path_str)
        cap = cv2.VideoCapture(video_path_str)
        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps == 0 or not cap.isOpened():
            raise ValueError(f"⚠️ Failed to open or read FPS from: {video_file}")

        output_subfolder = os.path.join(output_folder, os.path.splitext(video_file)[0])
        os.makedirs(output_subfolder, exist_ok=True)

        second_frame_counter = defaultdict(int)
        success, image = cap.read()
        frame_number = 0

        while success:
            if frame_number % max(1, int(fps // self.frame_rate)) == 0:
                seconds = int(frame_number / fps)
                timestamp = str(timedelta(seconds=seconds)).replace(":", "-")

                second_frame_counter[timestamp] += 1
                index = second_frame_counter[timestamp]

                output_filename = os.path.join(output_subfolder, f"{timestamp}_{index}.jpg")
                cv2.imwrite(output_filename, image)

            success, image = cap.read()
            frame_number += 1

        cap.release()