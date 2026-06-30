import tiktoken

encoding= tiktoken.encoding_for_model("gpt-4.1-mini")

def chunk_transcript(
            transcript:str,
            chunk_size=500,
            overlap=100

):
    tokens=encoding.encode(transcript)

    chunks=[]

    start=0

    while start<len(tokens):
         end = start + chunk_size

         chunk_tokens = tokens[start:end]

         chunk_text = encoding.decode(chunk_tokens)

         chunks.append(chunk_text)

         start += chunk_size - overlap
    return chunks     