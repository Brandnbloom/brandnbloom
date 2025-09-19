# services/ai_client.py
import os
from providers.openai_provider import OpenAIProvider
from providers.gemini_provider import GeminiProvider
from providers.huggingface_provider import HuggingFaceProvider

# Provider map
PROVIDERS = {
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "huggingface": HuggingFaceProvider,
}

# Pick from .env
ACTIVE_PROVIDER = os.getenv("AI_PROVIDER", "openai")

def get_provider():
    provider_cls = PROVIDERS.get(ACTIVE_PROVIDER.lower(), OpenAIProvider)
    return provider_cls()

provider = get_provider()

# Unified functions
def generate_text(prompt: str, **kwargs) -> str:
    return provider.generate_text(prompt, **kwargs)

def generate_image(prompt: str, **kwargs) -> str:
    return provider.generate_image(prompt, **kwargs)

def analyze_text(text: str, task: str, **kwargs) -> str:
    return provider.analyze_text(text, task, **kwargs)
