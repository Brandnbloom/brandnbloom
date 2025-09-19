# providers/openai_provider.py
import os
from providers.base_provider import BaseProvider
import openai

class OpenAIProvider(BaseProvider):
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_text(self, prompt: str, **kwargs) -> str:
        resp = openai.ChatCompletion.create(
            model=kwargs.get("model", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 600),
            temperature=kwargs.get("temperature", 0.5),
        )
        return resp.choices[0].message.content

    def generate_image(self, prompt: str, **kwargs) -> str:
        # Replace with DALL·E if available
        return f"https://fake.openai.image/{prompt.replace(' ', '_')}.png"

    def analyze_text(self, text: str, task: str, **kwargs) -> str:
        if task == "grammar":
            prompt = f"Correct grammar: {text}"
        elif task == "humanize":
            prompt = f"Rewrite to sound natural: {text}"
        else:
            prompt = f"Analyze ({task}): {text}"
        return self.generate_text(prompt, **kwargs)
