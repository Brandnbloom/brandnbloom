# services/ai_client.py
import os
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")

def generate_text(prompt: str, max_tokens: int = 300, temperature: float = 0.2):
    if AI_PROVIDER == "openai":
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        resp = openai.ChatCompletion.create(model="gpt-4o", messages=[{"role":"user","content":prompt}], max_tokens=max_tokens, temperature=temperature)
        return resp.choices[0].message.content
    elif AI_PROVIDER == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-pro")
        return model.generate_content(prompt).text
    elif AI_PROVIDER == "huggingface":
        from transformers import pipeline
        generator = pipeline("text-generation", model=os.getenv("HF_MODEL","gpt2"))
        out = generator(prompt, max_length=max_tokens)
        return out[0]["generated_text"]
    else:
        return "AI_PROVIDER not configured"
