# services/seo_service.py
from collections import Counter
import re

def keyword_suggestions(seed: str, country: str = "in"):
    """
    Minimal keyword expansion using OpenAI or simple heuristics.
    For production, use Keyword APIs (Ahrefs, SEMrush, Ubersuggest, Google Keyword Planner, SerpAPI)
    """
    # Simple heuristic: ask OpenAI quickly
    from services.openai_client import generate_text
    prompt = f"Generate 15 keyword phrases (comma-separated) related to: {seed}. Short phrases only."
    resp = generate_text(prompt, max_tokens=200, temperature=0.4)
    # try to split by commas/newlines
    kw = re.split(r"[\n,]+", resp)
    return [k.strip() for k in kw if k.strip()][:15]

def keyword_density(text: str, keyword: str) -> dict:
    words = re.findall(r"\w+", text.lower())
    total = len(words)
    kw_count = sum(1 for w in words if w == keyword.lower())
    density = (kw_count / total) * 100 if total else 0
    return {"keyword": keyword, "count": kw_count, "total_words": total, "density_percent": round(density, 3)}

def rank_check_stub(url: str, keyword: str):
    # placeholder: use SERP API for accurate rank checks
    return {"message": "Use SerpAPI or Google Search Console API for accurate ranking data."}
