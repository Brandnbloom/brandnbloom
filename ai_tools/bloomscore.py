# ai_tools/bloomscore.py

from typing import Dict, List


def _bucket(score: int) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 60:
        return "Good"
    if score >= 40:
        return "Average"
    return "Needs Improvement"


def compute_bloomscore(profile: Dict) -> Dict:
    """
    Compute BloomScore™ from normalized inputs.
    All values must already be clean & numeric.
    """

    followers = max(profile.get("followers", 0), 0)
    engagement = min(max(profile.get("engagement_rate", 0), 0), 1)
    consistency = min(max(profile.get("posting_consistency", 0), 0), 1)

    # --- Scoring logic (stable + interpretable) ---
    follower_score = min(followers / 10000, 1) * 30      # max 30
    engagement_score = engagement * 40                   # max 40
    consistency_score = consistency * 30                 # max 30

    total = round(follower_score + engagement_score + consistency_score)
    total = min(total, 100)

    return {
        "title": "BloomScore",
        "score": total,
        "bucket": _bucket(total),
        "components": {
            "followers_score": round(follower_score, 2),
            "engagement_score": round(engagement_score, 2),
            "consistency_score": round(consistency_score, 2),
        },
        "recommendations": [
            "Post 3–4 times per week consistently",
            "Use reels and carousels for higher engagement",
            "Collaborate with niche micro-influencers",
            "Maintain a clear brand bio and highlights",
        ],
    }


def run(input_data: Dict) -> Dict:
    """
    Entry point required by tool registry
    """
    return compute_bloomscore(input_data)
