# ai_tools/audit_tools.py

from typing import Dict

def audit_profile(profile: Dict) -> Dict:
    """
    Returns a simple brand audit based on profile data.
    """
    followers = profile.get("followers", 0)
    engagement = profile.get("engagement_rate", 0)
    posts = profile.get("posts_per_week", 0)

    score = min(100, int(followers * 0.2 + engagement * 50 + posts * 10))

    recommendations = []
    if engagement < 0.05:
        recommendations.append("Increase engagement by posting more interactive content")
    if posts < 2:
        recommendations.append("Post at least 2–3 times per week for consistency")
    if followers < 1000:
        recommendations.append("Consider collaborations to grow followers")

    return {
        "score": score,
        "components": {
            "followers": followers,
            "engagement_rate": engagement,
            "posts_per_week": posts
        },
        "recommendations": recommendations
    }
