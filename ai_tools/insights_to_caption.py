# ai_tools/insights_to_caption.py

from ai_tools.caption_generator import generate_caption

def insights_to_caption(analysis: dict) -> str:
    """
    Converts BloomScore analysis into a clean, IG-ready caption.

    Parameters:
        analysis (dict): Output from analyze_profile(), including:
            - bloom_score
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

        bloom_score = analysis.get("bloom_score", "—")
        engagement_rate = analysis.get("engagement_rate", "—")
        reels_ratio = analysis.get("reels_ratio", "—")

        context = (
            f"BloomScore Pro v2 Insights 🌸\n\n"
            f"✨ Profile Score: {bloom_score}\n"
            f"📈 Engagement Rate: {engagement_rate}%\n"
            f"🎞 Reels : Posts Ratio → {reels_ratio}\n\n"
            f"🌼 Strengths: {strengths if strengths else 'No major strengths detected yet'}\n"
            f"🌱 Growth Opportunities: {opportunities if opportunities else 'Keep posting consistently!'}\n"
        )

        # Uses your deterministic caption generator
        caption = generate_caption(context)
        return caption

    except Exception as e:
        return f"✨ Growth insights will be ready soon — {e}"
