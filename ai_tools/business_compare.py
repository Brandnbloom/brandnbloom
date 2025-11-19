# brandnbloom/ai_tools/business_compare.py
"""
Business Comparison Engine — BloomScore Pro v2
Compare multiple Instagram handles on key metrics:
followers, engagement rate, aesthetics, caption tone, consistency, BloomScore etc.
"""

from bloominsight.scraper import fetch_public_profile
from bloominsight.analyzer import analyze_profile
from brandnbloom.bloomscore_pro_v2 import compute_bloomscore_v2


def compare_handles(handles: list[str]):
    """
    Compare multiple IG profiles and generate a ranking + summary.

    Returns:
        {
            "results": {handle: metrics},
            "leader_by_followers": handle,
            "leader_by_bloomscore": handle,
            "ranking_table": [...ordered list...]
        }
    """
    results = {}

    for h in handles:
        try:
            profile = fetch_public_profile(h)
            analysis = analyze_profile(profile)

            # BloomScore Pro evaluation
            bloom = compute_bloomscore_v2(profile)

            results[h] = {
                "followers": analysis.get("followers", 0),
                "engagement_rate": analysis.get("engagement_rate", 0),
                "hashtag_count": analysis.get("hashtag_count", 0),
                "post_frequency": analysis.get("post_frequency", 0),
                "brand_aesthetic_score": bloom["components"]["aesthetic"],
                "tone_score": bloom["components"]["tone"],
                "reels_mix": bloom["components"]["reels_mix"],
                "story_consistency": bloom["components"]["story_consistency"],
                "reach_quality": bloom["components"]["reach_quality"],
                "bloomscore": bloom["score"],
            }

        except Exception as e:
            results[h] = {"error": str(e)}

    # ---------- Leaderboards ----------
    valid = {h: v for h, v in results.items() if "error" not in v}

    leader_by_followers = (
        max(valid.items(), key=lambda x: x[1]["followers"])[0]
        if valid else None
    )

    leader_by_bloomscore = (
        max(valid.items(), key=lambda x: x[1]["bloomscore"])[0]
        if valid else None
    )

    # Ranking Table
    ranking_table = sorted(
        [
            {
                "handle": h,
                "followers": v["followers"],
                "engagement_rate": v["engagement_rate"],
                "bloomscore": v["bloomscore"],
            }
            for h, v in valid.items()
        ],
        key=lambda x: (x["bloomscore"], x["followers"]),
        reverse=True,
    )

    return {
        "results": results,
        "leader_by_followers": leader_by_followers,
        "leader_by_bloomscore": leader_by_bloomscore,
        "ranking_table": ranking_table,
    }
