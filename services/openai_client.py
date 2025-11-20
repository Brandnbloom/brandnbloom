# services/openai_client.py

import os
from openai import OpenAI
from typing import Optional

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in environment variables.")

# Initialize client
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_text(
    prompt: str,
    model: str = "gpt-4o",
    max_tokens: int = 600,
    temperature: float = 0.2
):
    """
    Generic text generation wrapper using the latest OpenAI chat API.
    Works for gpt-4o, o1, o3-mini, etc.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].message.content
