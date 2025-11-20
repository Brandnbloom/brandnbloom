# services/reputation_service.py

import requests
from bs4 import BeautifulSoup
from db import get_session
from models import Review
from services.ai_client import generate_text


def fetch_reviews(urls: list):
    """
    Fetch raw text from review pages and store minimal snippets.
    NOTE: Real reputation management requires platform APIs (Google, FB, Yelp).
    """
    results = []

    for u in urls:
        try:
            r = requests.get(u, timeout=8)
            r.raise_for_status()

            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text().strip()

            snippet = text[:200] if text else ""

            with get_session() as s:
                review = Review(
                    source=u,
                    author=None,
                    rating=None,
                    text=text[:500] if text else None,
                )
                s.add(review)
                s.commit()

            results.append({"url": u, "snippet": snippet})

        except Exception as e:
            results.append({"url": u, "error": str(e)})

    return results


def analyze_sentiment(texts: list):
    """
    Use LLM sentiment scoring for multiple texts.
    Output: positive / neutral / negative + score (-1 to 1).
    """
    prompt = (
        "Perform sentiment analysis on the following texts.\n"
        "For each entry, return:\n"
        "- sentiment: positive / neutral / negative\n"
        "- score between -1 and 1\n\n"
        "---\n" +
        "\n---\n".join(texts)
    )

    out = generate_text(prompt, max_tokens=250)
    return {"analysis": out}


def auto_respond(payload):
    """
    Auto-generate a professional reply to a customer review.
    payload = { review_text: str, tone: str(optional) }
    """
    tone = payload.get("tone", "professional")
    review_text = payload.get("review_text", "")

    prompt = (
        f"Write a polite, empathetic, and professional response "
        f"to the customer review below.\n"
        f"Tone: {tone}\n\n"
        f"Review:\n{review_text}\n\n"
        f"Keep it concise, positive, and customer-first."
    )

    reply = generate_text(prompt, max_tokens=150)
    return {"reply": reply}
