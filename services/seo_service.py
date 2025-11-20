# services/seo_service.py

import re
from collections import Counter
from services.openai_client import generate_text


def keyword_suggestions(seed: str, country: str = "in") -> list[str]:
    """
    Minimal keyword expansion using OpenAI.
    Production: Use Keyword APIs (Ahrefs, SEMrush, Ubersuggest, GKP, SerpAPI)
    """
    prompt = (
        f"Generate 15 keyword phrases (comma-separated) related to: {seed}. "
        f"Keep phrases short and actionable."
    )
    resp = generate_text(prompt, max_tokens=200, temperature=0.4)
    # split by comma or newline
    kw = re.split(r"[\n,]+", resp)
    return [k.strip() for k in kw if k.strip()][:15]


def keyword_density(text: str, keyword: str) -> dict:
    """
    Compute basic keyword density in a text.
    Returns: {keyword, count, total_words, density_percent}
    """
    words = re.findall(r"\w+", text.lower())
    total = len(words)
    kw_count = sum(1 for w in words if w == keyword.lower())
    density = (kw_count / total) * 100 if total else 0
    return {
        "keyword": keyword,
        "count": kw_count,
        "total_words": total,
        "density_percent": round(density, 3),
    }


def rank_check_stub(url: str, keyword: str) -> dict:
    """
    Placeholder for keyword ranking checks.
    In production, use SERP API or Google Search Console API.
    """
    return {
        "url": url,
        "keyword": keyword,
        "message": "Use SerpAPI or Google Search Console API for accurate ranking data."
    }
