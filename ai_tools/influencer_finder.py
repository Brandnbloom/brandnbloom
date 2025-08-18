# Simple influencer finder that ranks candidate handles by engagement rate and follower count.
from bloominsight.scraper import fetch_public_profile
from bloominsight.analyzer import analyze_profile

def find_influencers(handles: list[str], min_followers: int = 1000, top_n: int = 5):
    candidates = []
    for h in handles:
        try:
            profile = fetch_public_profile(h)
            a = analyze_profile(profile)
            score = a.get("engagement_rate",0) * 0.6 + (min(1, profile.get("followers",0)/10000) * 40)
            candidates.append({"handle": h, "followers": profile.get("followers",0), "engagement_rate": a.get("engagement_rate",0), "score": score})
        except Exception as e:
            candidates.append({"handle":h, "error":str(e)})
    candidates = sorted([c for c in candidates if "error" not in c and c["followers"]>=min_followers], key=lambda x: x["score"], reverse=True)
    return candidates[:top_n]
