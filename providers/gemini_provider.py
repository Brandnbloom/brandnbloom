# providers/gemini_provider.py
import os
from providers.base_provider import BaseProvider
import google.generativeai as genai

class GeminiProvider(BaseProvider):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")

    def generate_text(self, prompt: str, **kwargs) -> str:
        resp = self.model.generate_content(prompt)
        return resp.text

    def generate_image(self, prompt: str, **kwargs) -> str:
        # Gemini image gen is limited → could fallback to stability.ai later
        return f"https://fake.gemini.image/{prompt.replace(' ', '_')}.png"

    def analyze_text(self, text: str, task: str, **kwargs) -> str:
        return self.generate_text(f"Task={task}\n\n{text}")
