# services/ai_client.py

import os
import json
from functools import lru_cache

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")


# -----------------------------
# Provider Loaders (Lazy Import)
# -----------------------------

@lru_cache
def load_openai_client():
    try:
        from openai import OpenAI
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except Exception as e:
        raise RuntimeError(f"Failed to load OpenAI: {e}")


@lru_cache
def load_gemini_client():
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        from google.generativeai import GenerativeModel
        return GenerativeModel("gemini-pro")
    except Exception as e:
        raise RuntimeError(f"Failed to load Gemini: {e}")


@lru_cache
def load_huggingface_client():
    try:
        from transformers import pipeline
        model = os.getenv("HF_MODEL", "gpt2")
        return pipeline("text-generation", model=model)
    except Exception as e:
        raise RuntimeError(f"Failed to load HuggingFace: {e}")


# -----------------------------
# Main generate() Function
# -----------------------------
def generate_text(prompt: str, max_tokens: int = 300, temperature: float = 0.2):
    """Unified wrapper for multiple AI providers."""

    try:
        if AI_PROVIDER == "openai":
            client = load_openai_client()
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return resp.choices[0].message["content"]

        elif AI_PROVIDER == "gemini":
            model = load_gemini_client()
            result = model.generate_content(prompt)
            return result.text

        elif AI_PROVIDER == "huggingface":
            generator = load_huggingface_client()
            result = generator(prompt, max_length=max_tokens)
            return result[0]["generated_text"]

        else:
            return f"Invalid AI_PROVIDER: {AI_PROVIDER}"

    except Exception as e:
        return f"AI Error ({AI_PROVIDER}): {str(e)}"
