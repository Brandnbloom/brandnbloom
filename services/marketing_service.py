# services/marketing_service.py

import re
from services.openai_client import generate_text


def generate_hashtags(caption: str, platform: str = "instagram"):
    """
    Generate up to 15 relevant & trending hashtags for the given caption.

    Uses OpenAI to propose hashtags and extracts them safely.
    """

    prompt = (
        f"Generate 15 relevant, trending, and high-reach hashtags for {platform}. "
        f"Caption: {caption}\n"
        "Return only hashtags separated by spaces or commas."
    )

    resp = generate_text(prompt, max_tokens=150, temperature=0.6)

    # Extract hashtags reliably
    hashtags = re.findall(r"#\w+", resp)

    # If AI didn't return # tags, fall back on splitting
    if not hashtags:
        possible = re.split(r"[,\n ]+", resp)
        hashtags = [t.strip() for t in possible if t.strip().startswith("#")]

    # Final sanitization (remove duplicates, ensure max 15)
    hashtags = list(dict.fromkeys(hashtags))  # preserves order, removes dupes

    return hashtags[:15]


def content_score_stub(content: dict):
    """
    Quick content scoring stub.
    Real production scoring may include:
    - Flesch Reading Ease
    - Keyword density
    - Sentiment analysis
    - CTA scoring
    - Formatting strength
    """

    body = content.get("body", "").strip()

    if not body:
        return {"score": 0, "notes": ["Content body empty."]}

    word_count = len(body.split())

    # Naive scoring: scale 0–100 based on word count (ideal ~200–250 words)
    raw_score = min(word_count / 2, 100)

    notes = [
        "This is a placeholder scoring system.",
        "Integrate Flesch-Kincaid readability, sentiment, keyword match, and CTA scoring in production."
    ]

    return {
        "score": round(raw_score, 1),
        "notes": notes
    }
