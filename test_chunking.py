from app.services.chunking import chunk_transcript

text = """
Artificial intelligence is transforming software engineering.

Companies use RAG systems.

Embeddings enable semantic search.

Large language models answer questions using retrieved context.

""" * 100

chunks = chunk_transcript(text)

print("Number of chunks:", len(chunks))

print()

print(chunks[0])

print()

print("---------------")

print()

print(chunks[1])