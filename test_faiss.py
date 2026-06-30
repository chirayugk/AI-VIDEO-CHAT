from app.services.chunking import chunk_transcript
from app.services.embedding import generate_embedding
from app.services.vector_store import *

text = """
Artificial Intelligence is transforming healthcare.

Embeddings are numerical representations.

FAISS performs semantic search.

Large Language Models answer questions.

""" * 100

chunks = chunk_transcript(text)

embeddings = []

for chunk in chunks:

    embeddings.append(
        generate_embedding(chunk)
    )

index = create_index(
    embeddings
)

save_index(
    index,
    "faiss_indexes/video_test.index"
)

print("Index Saved!")

index = load_index(
    "faiss_indexes/video_test.index"
)

question = "How does semantic search work?"

query_embedding = generate_embedding(
    question
)

distances, indices = search_index(
    index,
    query_embedding
)

print(indices)