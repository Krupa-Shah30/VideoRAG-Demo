from searcher import MultimodalSearcher
#from OllamaService import call_llm
from embedder import EmbeddingProcessor
from llm_response_generator import LLMResponder 
from qdrant_handler import QdrantHandler
import config
from dotenv import load_dotenv
import os

# 🧠 Initialize once here (hardcoded setup)
embedder_model = EmbeddingProcessor(config.EMBEDDING_MODEL)
qdrant_client = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)

def final_pipeline(Query, video_hash=None):
    """
    Final pipeline to perform multimodal search and LLM call.
    If video_hash is provided, restrict search to that video.
    """
    print("final_pipeline called with:", Query, video_hash)
    print("🔍 Performing search...")
    Video_Transcript = MultimodalSearcher(
        qdrant_handler=qdrant_client,
        embedder=embedder_model,
        collection_name=config.COLLECTION_NAME
    )

    # If video_hash is provided, pass it to the searcher
    if video_hash:
        similarity_search_results = Video_Transcript.search(query=Query, video_hash=video_hash)
    else:
        similarity_search_results = Video_Transcript.search(query=Query)

    if similarity_search_results is None:
        print("No relevant results found for the query and video_hash.")
        return {"error": "No relevant context found for your query. Please try a different question or check your video data."}

    print("💬 Calling LLM...")
    Output_generation=LLMResponder()
    final_output = Output_generation.call_llm(Query,similarity_search_results)
    
    return final_output

if __name__ == "__main__":
    Query = "Tell me more about storage and processing in a computer."
    result=final_pipeline(Query)
    print("Final Output:", result)












