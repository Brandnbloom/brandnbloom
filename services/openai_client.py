# services/openai_client.py
import os
import openai
from typing import Optional

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in environment")

openai.api_key = OPENAI_API_KEY

def generate_text(prompt: str, model: str = "gpt-4o", max_tokens: int = 600, temperature: float = 0.2):
    """
    Generic text generation wrapper. Adjust model to your plan.
    """
    # NOTE: if your account uses different model id, change it.
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"user","content":prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content
