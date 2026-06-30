from app.services.chunking import chunk_transcript
from app.services.embedding import generate_embedding

text = """
Artificial Intelligence is transforming healthcare.

Embeddings help semantic search.

FAISS stores vectors efficiently.

""" * 50

chunks = chunk_transcript(text)

print("Chunks:", len(chunks))

embeddings = []

for chunk in chunks:

    vector = generate_embedding(chunk)

    embeddings.append(vector)

print("Embeddings Generated:", len(embeddings))

print("Vector Dimension:", len(embeddings[0]))