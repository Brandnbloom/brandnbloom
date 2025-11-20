# services/ example writer_service.py

from services.ai_client import generate_text, analyze_text


def generate_seo_article(title: str, keywords: list[str], length: int = 600) -> str:
    """
    Generate a long-form SEO article with headings, structure, and keyword placement.
    """
    keyword_str = ", ".join(keywords)

    prompt = (
        f"Write a well-structured SEO article of around {length} words on '{title}'. "
        f"Naturally include the keywords: {keyword_str}. "
        "Use headings, subheadings, bullet points, examples, and keep it easy to read."
    )

    return generate_text(prompt, max_tokens=length * 2)


def paraphrase_text(text: str) -> str:
    """
    Paraphrase text while keeping meaning intact.
    """
    return analyze_text(text, mode="paraphrase")


def grammar_check(text: str) -> dict:
    """
    Return grammar-corrected text along with original.
    """
    corrected = analyze_text(text, mode="grammar")
    return {
        "original": text,
        "corrected": corrected
    }


def humanize_text(text: str) -> str:
    """
    Convert AI-sounding text into natural human tone.
    """
    return analyze_text(text, mode="humanize")
