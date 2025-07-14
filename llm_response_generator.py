# import openai

# class LLMResponder:
#     def __init__(self, api_key):
#         openai.api_key = api_key

#     def generate_answer(self, query, context_chunks):
#         context_text = "\n\n".join(context_chunks)
#         prompt = f"""You are a helpful assistant. Answer the question based only on the following context:

# {context_text}

# Question: {query}
# Answer:"""

#         response = openai.ChatCompletion.create(
#             model="gpt-4",  # or "gpt-3.5-turbo"
#             messages=[
#                 {"role": "system", "content": "You are a multimodal assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.3,
#             max_tokens=300
#         )

#         return response.choices[0].message["content"]

import os
import base64
from openai import OpenAI


class LLMResponder:
    def __init__(self):
        pass
    def call_llm(self, prompt: str, results_final:dict = None) -> str:    
        # print(results_final["text"])
        #print(results_final["images"])

        try:
            
            text_chunks = "\n\n".join(
        [
            f"Text Snippet {i + 1} [{item['timestamp']:.2f}s]:\n{item['text']}"
            for i, item in enumerate(results_final["text"])
        ]
    )
            timestamps = [item["timestamp"] for item in results_final["text"] if "timestamp" in item]
            start_ts =min(timestamps) if timestamps else None
            
            end_ts = max(timestamps) if timestamps else None

            print(timestamps,start_ts)
    # Build image references
            image_refs = "\n".join(
        [
            f"Image Frame {i + 1} (~{img.get('timestamp_guess', 0):.2f}s): {img['frame']}"
            for i, img in enumerate(results_final["images"])
        ]
    )
            client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
        )

       
       # Start with the textual context
            content_blocks = [
    {
        "type": "text",
        "text": f"""
You are an intelligent VideoRAG Interface that helps users answer questions based on long-form video content.

You are given:
- Transcript excerpts from the video
- Visual snapshots (frames)
Both were retrieved using semantic similarity from a vector database.

Use these to understand the user's intent and generate an accurate and concise answer.

User Question: "{prompt}"



Transcript Snippets:
{text_chunks}

Relevant Frame References (timestamps + filenames only, full visuals sent below):
{image_refs}
"""
    }
]

# Then append all actual image blocks
            for img in results_final["images"]:
                # Convert local image to base64
                image_path = img["path"]
                try:
                    with open(image_path, "rb") as image_file:
                        image_data = image_file.read()
                        base64_image = base64.b64encode(image_data).decode('utf-8')
                    
                    content_blocks.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    })
                except Exception as e:
                    print(f"⚠️ Failed to load image {image_path}: {e}")
                    # Skip this image if we can't load it
                    continue

            completion = client.chat.completions.create(
                model="qwen/qwen2.5-vl-72b-instruct:free",
                messages=[
        {
            "role": "user",
            "content": content_blocks
        }
    ]
)

            return {
                "synthesized_answer": completion.choices[0].message.content,
                "start_timestamp": start_ts
            }

        except Exception as error:
            print("Error calling LLM:", str(error))
            raise
