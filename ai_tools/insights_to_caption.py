# ai_tools/insights_to_caption.py

from ai_tools.caption_generator import generate_caption

def insights_to_caption(analysis: dict) -> str:
    """
    Converts BloomScore analysis into a clean, IG-ready caption.
    
    Parameters:
        analysis (dict): Output from analyze_profile(), including:
            - aesthetics_score
            - reels_ratio
            - engagement_rate
            - saves
            - shares
            - strengths
            - opportunities
    
    Returns:
        str: Instagram-optimized caption.
    """

    try:
        strengths = ", ".join(analysis.get("strengths", []))
        opportunities = ", ".join(analysis.get("opportunities", []))

        context = (
            f"Your profile scored {analysis.get('bloom_score', '—')} on BloomScore Pro v2. "
            f"Strong areas: {strengths if strengths else '—'}. "
            f"Growth opportunities: {opportunities if opportunities else '—'}. "
            f"Engagement rate: {analysis.get('engagement_rate', '—')}%. "
            f"Reels vs Posts Mix: {analysis.get('reels_ratio', '—')}."
        )

        caption = generate_caption(context, tone="aesthetic, brand-friendly, high-engagement")
        return caption

    except Exception as e:
        return f"✨ Growth insights coming soon — {e}"
