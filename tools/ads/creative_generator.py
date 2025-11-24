# tools/ads/creative_generator.py

from utils.ai_client import generate_text


def generate_ad_creatives(
    platform: str,
    product: str,
    tone: str = "Professional",
    count_headlines: int = 10,
    count_descriptions: int = 6,
    count_cta: int = 6,
    count_images: int = 3
):
    """
    Generate headlines, descriptions, CTAs, and image prompt ideas
    for ad campaigns using the AI client.
    """

    prompt = (
        f"Generate ad creatives for the following:\n"
        f"Platform: {platform}\n"
        f"Product description: {product}\n"
        f"Tone: {tone}\n\n"
        f"Required Output:\n"
        f"- {count_headlines} catchy ad headlines\n"
        f"- {count_descriptions} short ad descriptions\n"
        f"- {count_cta} strong call-to-actions (CTAs)\n"
        f"- {count_images} image prompt ideas suitable for {platform}\n\n"
        f"Format the answer clearly with sections."
    )

    response = generate_text(prompt, max_tokens=600)
    return response
