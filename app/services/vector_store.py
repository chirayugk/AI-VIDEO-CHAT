import faiss
import numpy as np
import json
import os


def create_index(embeddings):

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    vectors = np.array(
        embeddings,
        dtype=np.float32
    )

    index.add(vectors)

    return index

def save_index(index, path):

    faiss.write_index(
        index,
        path
    )

def load_index(path):

    return faiss.read_index(path)

def search_index(
    index,
    query_embedding,
    top_k=5
):

    query = np.array(
        [query_embedding],
        dtype=np.float32
    )

    distances, indices = index.search(
        query,
        top_k
    )

    return distances, indices    

def save_chunks(chunks, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=4
        )

def ensure_directory():

    os.makedirs(
        "faiss_indexes",
        exist_ok=True
    )        