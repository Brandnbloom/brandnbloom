# services/design_service.py

import os
from urllib.parse import quote
from services.ai_client import generate_text


# -------------------------------------------------------------------
# GENERATE IMAGE (placeholder + refined prompt)
# -------------------------------------------------------------------
def generate_image_from_prompt(prompt: str, size: str = "1024x1024") -> dict:
    """
    Generates an AI image (placeholder for now).
    Uses AI to refine the prompt and returns a mock URL.
    Replace with real API integrations (DALL·E, Midjourney, Stability.ai).
    """

    # Refine prompt using your AI provider (OpenAI/Gemini/HF)
    refined_prompt = generate_text(
        f"Refine this image prompt to be more cinematic, vivid and studio-quality:\n\n{prompt}",
        max_tokens=150
    )

    # Placeholder output (swap later)
    placeholder_url = (
        f"https://placeholder.image/api?"
        f"refined_prompt={quote(refined_prompt)}&size={size}"
    )

    return {
        "input_prompt": prompt,
        "refined_prompt": refined_prompt,
        "image_url": placeholder_url
    }


# -------------------------------------------------------------------
# CANVA TEMPLATE STUB
# -------------------------------------------------------------------
def create_canva_template_stub():
    """
    Stub for future Canva integration.
    Canva provides APIs via Partnerships — this placeholder explains that.
    """

    return {
        "status": "stub",
        "message": (
            "This endpoint will eventually integrate with Canva's Partner API. "
            "You will be able to: create templates, duplicate brand kits, and "
            "auto-generate editable designs. Contact Canva Developer Relations for access."
        )
    }
