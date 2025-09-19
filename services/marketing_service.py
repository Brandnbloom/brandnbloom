# services/marketing_service.py
from services.openai_client import generate_text
import re

def generate_hashtags(caption: str, platform: str = "instagram"):
    prompt = f"Generate 15 relevant and trending hashtags for this caption on {platform}. Caption: {caption}"
    resp = generate_text(prompt, max_tokens=120, temperature=0.6)
    # split out hashtags
    tags = re.findall(r"#\w+", resp)
    if not tags:
        tags = [t.strip() for t in re.split(r",|\n", resp) if t.strip()]
    return tags[:15]

def content_score_stub(content: dict):
    # quick scoring: readability, length, CTA presence — use real readability libs in production
    body = content.get("body","")
    score = len(body.split())/200  # naive
    return {"score": min(round(score*100,1), 100), "notes": ["Integrate Flesch reading ease, sentiment, keyword match in prod."]}
