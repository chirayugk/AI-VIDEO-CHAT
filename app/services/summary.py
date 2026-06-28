from openai import OpenAI

from ..conifg import OPENAI_API_KEY

import json

client=OpenAI(
    api_key=OPENAI_API_KEY
)


def generate_summary(transcript):

    prompt=f"""
         You are an expert meeting summarizer.

        Given the transcript below, return JSON only.

        {{
        "summary":"...",
        "key_takeaways":[
        "...",
        "...",
        "..."
        ],
        "topics":[
        "...",
        "..."
        ]
        }}

        Transcript:

        {transcript}
            """
    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
         response_format={
            "type":"json_object"
        }
    )
    return json.loads(
        response.choices[0].message.content
    )