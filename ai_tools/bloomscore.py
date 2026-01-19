"""
bloomscore.py
Computes the BloomScore™ for a social media profile using:
- Engagement Rate (40%)
- Posting Consistency (20%)
- Hashtag Variety (15%)
- Brand Health (Bio + Logo) (15%)
- Growth Trend (10%)

Dependencies:
- bloominsight.analyzer.analyze_profile
- bloominsight.utils.engagement_rate
"""

from bloominsight.analyzer import analyze_profile
from bloominsight.utils.engagement import engagement_rate


def _categorize(score: int) -> str:
    """Return qualitative bucket based on score."""
    if score >= 80:
        return "Excellent"
    if score >= 60:
        return "Good"
    if score >= 40:
        return "Fair"
        # Anything below becomes Needs Work
    return "Needs Work"


def _posting_consistency(posts_per_week: float) -> int:
    """
    Posting consistency scoring:
    20 → 4+ posts/week  
    15 → 2–3 posts/week  
    10 → 1 post/week  
    5 → inactive/less than 1  
    """
    if posts_per_week >= 4:
        return 20
    if posts_per_week >= 2:
        return 15
    if posts_per_week >= 1:
        return 10
    return 5


def _hashtag_variety(count: int) -> int:
    """
    Hashtag variety score:
    15 → 6+ unique hashtags used
    10 → 3–5
    5  → <3
    """
    if count >= 6:
        return 15
    if count >= 3:
        return 10
    return 5


def _brand_health_score(score: float) -> int:
    """
    Brand health from analyzer:
    15 → strong, 10 → moderate, 5 → weak
    """
    if score >= 70:
        return 15
    if score >= 40:
        return 10
    return 5


def _growth_trend(followers_history: list) -> int:
    """
    Simple growth metric based on last 7–30 days.  
    For now, placeholder logic:
      10 → >5% growth  
      7  → 1–5%  
      4  → stable  
      2  → shrinking  
    """
    if not followers_history or len(followers_history) < 2:
        return 4  # neutral

    initial = followers_history[0]
    latest = followers_history[-1]

    if initial <= 0:
        return 4

    growth_pct = ((latest - initial) / initial) * 100

    if growth_pct > 5:
        return 10
    if growth_pct >= 1:
        return 7
    if growth_pct >= 0:
        return 4
    return 2


def compute_bloomscore(profile: dict) -> dict:
    """Compute BloomScore based on profile analytics."""
    try:
        analysis = analyze_profile(profile)
    except Exception:
        analysis = {}

    # COMPONENTS ---------------------------------------------------
    er = analysis.get("engagement_rate", 0)          # 0–100
    posts_per_week = analysis.get("posts_per_week", 0)
    hashtag_count = analysis.get("hashtag_count", 0)
    brand_health = analysis.get("brand_health_score", 0)
    followers_history = analysis.get("followers_history", [])

    # Scores --------------------------------------------------------
    er_score = er * 0.4                               # 40%
    posting_score = _posting_consistency(posts_per_week)  # 20
    hashtag_score = _hashtag_variety(hashtag_count)       # 15
    brand_score = _brand_health_score(brand_health)       # 15
    growth_score = _growth_trend(followers_history)       # 10

    total = er_score + posting_score + hashtag_score + brand_score + growth_score
    score = min(100, int(total))

    bucket = _categorize(score)

    return {
        "score": score,
        "bucket": bucket,
        "components": {
            "engagement_rate": er,
            "er_weighted": round(er_score, 2),
            "posting_consistency": posting_score,
            "hashtag_variety": hashtag_score,
            "brand_health": brand_score,
            "growth": growth_score
        },
        "analysis": analysis
    }
