def generate_caption(insight, tone="professional", platform="Instagram"):
    base = f"""
You are a brand strategist.
Convert this insight into a high-performing {platform} caption.

Insight:
{insight}

Tone: {tone}
Include CTA.
"""

    return base  # later sent to LLM
