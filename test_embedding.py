from app.services.embedding import generate_embedding

vector = generate_embedding(
    "Artificial intelligence is transforming software engineering."
)

print(type(vector))

print(len(vector))

print(vector[:10])