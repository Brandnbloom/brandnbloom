"""
bloomscore.py
Computes the BloomScore™ for a social media profile using:
- Engagement Rate (40%)
- Posting Consistency (20%)
- Hashtag Variety (15%)
- Brand Health (15%)
- Growth Trend (10%)

NO external dependencies.
"""

# ---------------------------------------------------
# Helpers
# ---------------------------------------------------

def _categorize(score: int) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 60:
        return "Good"
    if score >= 40:
        return "Fair"
    return "Needs Work"


def _posting_consistency(posts_per_week: float) -> int:
    if posts_per_week >= 4:
        return 20
    if posts_per_week >= 2:
        return 15
    if posts_per_week >= 1:
        return 10
    return 5


def _hashtag_variety(count: int) -> int:
    if count >= 6:
        return 15
    if count >= 3:
        return 10
    return 5


def _brand_health_score(score: float) -> int:
    if score >= 70:
        return 15
    if score >= 40:
        return 10
    return 5


def _growth_trend(followers_history: list) -> int:
    if not followers_history or len(followers_history) < 2:
        return 4

    start = followers_history[0]
    end = followers_history[-1]

    if start <= 0:
        return 4

    growth_pct = ((end - start) / start) * 100

    if growth_pct > 5:
        return 10
    if growth_pct >= 1:
        return 7
    if growth_pct >= 0:
        return 4
    return 2


# ---------------------------------------------------
# Main API
# ---------------------------------------------------

def compute_bloomscore(profile: dict) -> dict:
    """
    Expected profile format:
    {
        "engagement_rate": float (0–100),
        "posts_per_week": float,
        "hashtag_count": int,
        "brand_health_score": float (0–100),
        "followers_history": list[int]
    }
    """

    er = profile.get("engagement_rate", 0)
    posts_per_week = profile.get("posts_per_week", 0)
    hashtag_count = profile.get("hashtag_count", 0)
    brand_health = profile.get("brand_health_score", 0)
    followers_history = profile.get("followers_history", [])

    er_score = er * 0.4
    posting_score = _posting_consistency(posts_per_week)
    hashtag_score = _hashtag_variety(hashtag_count)
    brand_score = _brand_health_score(brand_health)
    growth_score = _growth_trend(followers_history)

    total = er_score + posting_score + hashtag_score + brand_score + growth_score
    score = min(100, int(total))

    return {
        "score": score,
        "bucket": _categorize(score),
        "components": {
            "engagement_rate": er,
            "posting_consistency": posting_score,
            "hashtag_variety": hashtag_score,
            "brand_health": brand_score,
            "growth_trend": growth_score,
        }
    }
