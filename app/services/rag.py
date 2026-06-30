import json

from openai import OpenAI

from ..conifg import OPENAI_API_KEY

from .embedding import generate_embedding

from .vector_store import load_index, search_index

client = OpenAI(api_key=OPENAI_API_KEY)

def load_chunks(path):

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)


def retrieve_context(video_id, question):

    index = load_index(
        f"faiss_indexes/video_{video_id}.index"
    )

    chunks = load_chunks(
        f"faiss_indexes/video_{video_id}_chunks.json"
    )

    query_embedding = generate_embedding(question)

    distances, indices = search_index(
        index,
        query_embedding,
        top_k=5
    )

    retrieved = []

    for i in indices[0]:

        if i != -1:

            retrieved.append(
                chunks[i]
            )

    return retrieved


def answer_question(video_id, question):

    context = retrieve_context(
        video_id,
        question
    )

    prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

If the answer is not present in the context, reply:

"I couldn't find this information in the uploaded video."

Context:

{chr(10).join(context)}

Question:

{question}
"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content