# ai_tools/bloomscore.py

def compute_bloomscore(profile: dict) -> dict:
    """
    Expected normalized inputs:
    followers_score: 0–100
    engagement_rate: 0–100
    posting_consistency: 0–100
    """

    followers = profile.get("followers_score", 0)
    engagement = profile.get("engagement_rate", 0)
    consistency = profile.get("posting_consistency", 0)

    score = (
        followers * 0.3 +
        engagement * 0.4 +
        consistency * 0.3
    )

    score = min(round(score), 100)

    if score >= 80:
        bucket = "Excellent"
    elif score >= 60:
        bucket = "Good"
    elif score >= 40:
        bucket = "Average"
    else:
        bucket = "Needs Improvement"

    return {
        "score": score,
        "bucket": bucket,
        "components": {
            "followers_score": followers,
            "engagement_rate": engagement,
            "posting_consistency": consistency,
        },
        "analysis": {
            "recommendations": [
                "Post consistently 3–4 times per week",
                "Use short-form video (Reels)",
                "Collaborate with micro-influencers",
            ]
        }
    }
