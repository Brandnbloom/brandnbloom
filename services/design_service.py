# services/design_service.py
import os
from services.openai_client import generate_text

def generate_image_from_prompt(prompt: str, size: str = "1024x1024") -> str:
    """
    Example: produce an image using an external image generation API.
    For quick dev, we will ask OpenAI to create a prompt and return a placeholder URL.
    Replace with actual call to Stability.ai, Midjourney, DALL·E or a hosted image API.
    """
    # For demo we just return a generated prompt + a placeholder
    refined_prompt = generate_text(f"Refine this image prompt to be art-director friendly: {prompt}", max_tokens=120)
    # Replace below with real API call:
    placeholder_url = f"https://placeholder.images/ai?prompt={refined_prompt.replace(' ','%20')}"
    return placeholder_url

def create_canva_template_stub():
    return "This endpoint should connect to Canva's API or a custom drag-drop builder. Canva has partner APIs for templates."
