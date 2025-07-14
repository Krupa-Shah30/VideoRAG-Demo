from qdrant_client import QdrantClient
import config

client = QdrantClient(url=config.QDRANT_URL)

scroll = client.scroll(
    collection_name=config.COLLECTION_NAME,
    limit=5,  # get a few
    with_payload=True
)

print("✅ ✅ ✅ Example payloads in Qdrant:")
video_hashes = set()
for p in scroll[0]:
    print(p.payload)
    if 'video_hash' in p.payload:
        video_hashes.add(p.payload['video_hash'])
print("All unique video_hash values in Qdrant:", video_hashes)
