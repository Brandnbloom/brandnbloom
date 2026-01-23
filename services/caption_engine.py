
def generate_caption(insight, tone="professional", platform="Instagram"):
    prompt = f"""
You are a brand strategist.

Create a high-performing {platform} caption based on this insight:

{insight}

Tone: {tone}
Add a strong CTA.
"""
    return prompt
