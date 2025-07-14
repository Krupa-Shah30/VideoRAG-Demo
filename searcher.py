import json
from IPython.display import Image as IPyImage, display
from utils import extract_frame_time_from_filename
import config

class MultimodalSearcher:
    def __init__(self, qdrant_handler, embedder, collection_name=None):
        self.qdrant = qdrant_handler
        self.embedder = embedder
        self.collection_name = collection_name or config.COLLECTION_NAME

    def search(self, query, top_k=None, min_score=None, video_hash=None):
        top_k = top_k or config.TOP_K if hasattr(config, "TOP_K") else 5
        min_score = min_score or config.MIN_SCORE if hasattr(config, "MIN_SCORE") else 0

        print(f"🔍 Running multimodal search for: \"{query}\"")
        print(f"DEBUG: Query video_hash: {video_hash}")
        query_vec = self.embedder.embed_text(query)

        # ✅ Pass hash so Qdrant filters at the DB level
        results = self.qdrant.search(query_vec, top_k=top_k * 20, video_hash=video_hash)

        text_results = []
        image_results = []

        for res in results:
            payload = res.payload
            print("DEBUG: payload video_hash:", payload.get("video_hash"), "score:", res.score)
            try:
                content = json.loads(payload.get("_node_content", "{}"))
            except json.JSONDecodeError:
                print("⚠️ Skipping result with malformed _node_content.")
                continue

            node_type = payload.get("type", "").lower()

            # ✅ Safe fallback double-check
            if video_hash and payload.get("video_hash") != video_hash:
                continue

            if node_type == "text":
                text_results.append({
                    "text": content.get("text", ""),
                    "timestamp": float(payload.get("timestamp", 0)),
                    "video_id": payload.get("video_id", "unknown"),
                    "score": res.score
                })

            elif node_type == "image":
                image_path = content.get("image") or payload.get("image_path", "")
                if not image_path:
                    print("⚠️ Image path missing for an image node. Skipping.")
                    continue

                frame = payload.get("source", "")
                ts_guess = extract_frame_time_from_filename(frame)

                image_results.append({
                    "path": image_path,
                    "frame": frame,
                    "video_id": payload.get("video_id", "unknown"),
                    "timestamp_guess": ts_guess if ts_guess else -1,
                    "score": res.score
                })

            else:
                print(f"⚠️ Unknown node type '{node_type}' in result. Skipping.")

        valid_text = sorted(
            [t for t in text_results if t["score"] >= min_score],
            key=lambda x: -x["score"]
        )
        valid_images = sorted(
            [i for i in image_results if i["score"] >= min_score],
            key=lambda x: -x["score"]
        )

        if not valid_text and not valid_images:
            print(f"❌ No relevant text or images found (score < {min_score}).")
            return

        final_text = []
        final_images = []

        print(f"\n✅ Top {top_k} Text Results:")
        for text_node in valid_text[:top_k]:
            print(f"[📝 TEXT] (Video: {text_node['video_id']}, Time: {text_node['timestamp']:.2f}s, Score: {text_node['score']:.4f})")
            print(text_node["text"])
            final_text.append(text_node)
            print("—" * 60)

        print(f"\n🖼️ Top {top_k} Image Results:")
        for image_node in valid_images[:top_k]:
            if not image_node["path"]:
                print(f"⚠️ Skipping image with missing path. Frame: {image_node['frame']}")
                continue
            print(f"[🖼️ IMAGE] (Video: {image_node['video_id']}, ~{image_node['timestamp_guess']:.2f}s, Score: {image_node['score']:.4f})")
            print(f"Frame: {image_node['frame']}")
            final_images.append(image_node)
            try:
                display(IPyImage(image_node["path"]))
            except Exception as e:
                print(f"⚠️ Failed to display image: {e}")
            print("—" * 60)

        final_output = {
            "text": final_text,
            "images": final_images
        }
        return final_output
