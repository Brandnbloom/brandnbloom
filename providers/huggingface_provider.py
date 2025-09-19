# providers/huggingface_provider.py
import os
from providers.base_provider import BaseProvider
from transformers import pipeline

class HuggingFaceProvider(BaseProvider):
    def __init__(self):
        self.generator = pipeline("text-generation", model=os.getenv("HF_MODEL", "gpt2"))

    def generate_text(self, prompt: str, **kwargs) -> str:
        out = self.generator(prompt, max_length=kwargs.get("max_tokens", 200), num_return_sequences=1)
        return out[0]["generated_text"]

    def generate_image(self, prompt: str, **kwargs) -> str:
        # HF has diffusion models but heavy; integrate diffusers if needed
        return f"https://fake.hf.image/{prompt.replace(' ', '_')}.png"

    def analyze_text(self, text: str, task: str, **kwargs) -> str:
        return f"Task={task} not implemented for HuggingFace local yet"
