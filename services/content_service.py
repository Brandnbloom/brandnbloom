# services/content_service.py
from services.ai_client import generate_text

def optimize_content(title: str, body: str):
    prompt = f"""
You are a content optimization assistant.
Title: {title}
Content:
{body}

Give:
1) SEO-friendly headline options (5)
2) Meta description (<=160 chars)
3) Suggestions to improve readability, headings, keyword placement, internal linking.
4) Short checklist of actionable items.
Respond in JSON.
"""
    out = generate_text(prompt, max_tokens=600)
    return {"suggestions": out}

def analyze_readability(body: str):
    prompt = f"Analyze readability, grade level, and provide short fixes: {body}"
    return {"analysis": generate_text(prompt, max_tokens=300)}
