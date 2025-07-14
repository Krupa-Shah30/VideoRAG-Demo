from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core.schema import TextNode, ImageNode
import os
import config
from PIL import Image
import re

class TextImageIndexer:
    def __init__(self, embedder, chunk_size=200, chunk_overlap=50, video_hash=None):
        self.embedder = embedder
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self.video_hash = video_hash  # ✅ Store the video hash for later use

    def index_text(self, transcript_dir):
        """
        - Splits transcript files into chunks using real timestamps from transcript
        - Embeds them
        - Wraps in TextNode objects with metadata
        """
        nodes = []
        timestamp_pattern = re.compile(r"\[(\d+\.?\d*)s\]\s*(.*)")

        for fname in os.listdir(transcript_dir):
            if not fname.endswith(".txt"):
                continue

            path = os.path.join(transcript_dir, fname)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            video_id = os.path.splitext(fname)[0]

            for i, line in enumerate(lines):
                match = timestamp_pattern.match(line)
                if not match:
                    continue
                timestamp = float(match.group(1))
                text = match.group(2).strip()
                if not text:
                    continue

                embedding = self.embedder.embed_text(text)
                node = TextNode(
                    text=text,
                    metadata={
                        "type": "text",
                        "video_id": video_id,
                        "video_hash": self.video_hash,  # ✅ Include hash here
                        "source": fname,
                        "chunk_index": i,
                        "timestamp": timestamp  # Use real timestamp!
                    }
                )
                node.embedding = embedding
                nodes.append(node)
        return nodes

    def index_images(self, frame_dir):
        """
        - Loads each .jpg image
        - Embeds them
        - Wraps in ImageNode objects with metadata
        """
        nodes = []
        for folder in os.listdir(frame_dir):
            folder_path = os.path.join(frame_dir, folder)
            if os.path.isdir(folder_path):
                for img_file in os.listdir(folder_path):
                    if img_file.endswith(".jpg"):
                        img_path = os.path.join(folder_path, img_file)
                        embedding = self.embedder.embed_image(img_path)
                        node = ImageNode(
                            image=img_path,
                            metadata={
                                "type": "image",
                                "video_id": folder,
                                "video_hash": self.video_hash,  # ✅ Include hash here
                                "source": img_file,
                                "image_path": img_path
                            }
                        )
                        node.embedding = embedding
                        nodes.append(node)
        return nodes
