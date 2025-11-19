# ai_tools/influencer_finder.py
# Simple influencer finder that ranks candidate handles by engagement rate and follower count.
# Updated for BloomScore Pro v2 with cleaner scoring and stronger error handling.

from typing import List, Dict
from bloominsight.scraper import fetch_public_profile
from bloominsight.analyzer import analyze_profile


def find_influencers(handles: List[str], min_followers: int = 1000, top_n: int = 5) -> List[Dict]:
    """
    Identify promising influencers based on Engagement Rate + scaled follower score.
    Returns a list of influencer dicts sorted by score.

    Scoring Formula (0–100):
    - ER Weight (60%): Higher engagement = better
    - Follower Weight (40%): Scaled from 0 to 40 (10k+ gets full score)

    Parameters:
        handles: List of Instagram handles
        min_followers: Minimum follower threshold
        top_n: Number of top influencers to return
    """
    candidates = []

    for handle in handles:
        try:
            profile = fetch_public_profile(handle)
            analysis = analyze_profile(profile)

            followers = profile.get("followers", 0)
            er = analysis.get("engagement_rate", 0)

            # Normalize follower score (maxes at 10k)
            follower_score = min(1, followers / 10000) * 40

            # Composite BloomScore-like influence score
            score = (er * 0.6) + follower_score

            candidates.append({
                "handle": handle,
                "followers": followers,
                "engagement_rate": er,
                "score": round(score, 2)
            })

        except Exception as e:
            candidates.append({
                "handle": handle,
                "error": str(e)
            })

    # Filter out failures + apply minimum followers + sort
    valid = [
        c for c in candidates
        if "error" not in c and c.get("followers", 0) >= min_followers
    ]

    sorted_candidates = sorted(valid, key=lambda x: x["score"], reverse=True)

    return sorted_candidates[:top_n]
