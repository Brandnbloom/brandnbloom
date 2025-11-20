# services/content_service.py

from services.ai_client import generate_text
import json


# -------------------------------------------------------------
# 1. SEO CONTENT OPTIMIZATION
# -------------------------------------------------------------
def optimize_content(title: str, body: str, strict_json: bool = True):
    """
    Uses AI to optimize content:
    - SEO headline options
    - Meta description
    - Readability + keyword placement suggestions
    - Actionable checklist
    Returns JSON-safe structure.
    """

    prompt = (
        "You are an expert SEO content optimizer.\n\n"
        f"Title:\n{title}\n\n"
        f"Content:\n{body}\n\n"
        "Return a JSON object with the following keys:\n"
        "1. seo_headlines: list of 5 SEO-friendly headlines\n"
        "2. meta_description: string (<=160 characters)\n"
        "3. improvements: list of suggestions to improve readability, headings, keyword placement, internal linking\n"
        "4. checklist: list of short actionable items\n\n"
    )

    if strict_json:
        prompt += (
            "Important rules:\n"
            "- Response MUST be valid JSON only.\n"
            "- Do NOT add extra explanation.\n"
            "- Do NOT add markdown.\n"
        )

    raw = generate_text(prompt, max_tokens=700, temperature=0.3)

    # Try decoding JSON; if fails, return raw
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {"raw_output": raw, "error": "Invalid JSON returned by model"}

    return parsed


# -------------------------------------------------------------
# 2. READABILITY ANALYSIS
# -------------------------------------------------------------
def analyze_readability(body: str):
    """
    Produces a readability analysis + suggested improvements.
    """

    prompt = (
        "Analyze the readability of the following text.\n"
        "Provide:\n"
        "- Readability score (Flesch or equivalent)\n"
        "- Reading grade level\n"
        "- Issues (sentence length, clarity, jargon, structure)\n"
        "- Short recommended fixes\n\n"
        f"Text:\n{body}\n\n"
        "Respond in JSON only."
    )

    raw = generate_text(prompt, max_tokens=350, temperature=0.2)

    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {"raw_output": raw, "error": "Invalid JSON returned by model"}

    return parsed
