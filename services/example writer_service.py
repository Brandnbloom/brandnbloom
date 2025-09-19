# services/writer_service.py
from services.ai_client import generate_text, analyze_text

def generate_seo_article(title: str, keywords: list[str], length: int = 600) -> str:
    prompt = f"Write an SEO article (~{length} words) on '{title}' including {', '.join(keywords)}."
    return generate_text(prompt, max_tokens=length*2)

def paraphrase_text(text: str) -> str:
    return analyze_text(text, "paraphrase")

def grammar_check(text: str) -> dict:
    corrected = analyze_text(text, "grammar")
    return {"original": text, "corrected": corrected}

def humanize_text(text: str) -> str:
    return analyze_text(text, "humanize")
