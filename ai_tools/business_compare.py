# Compare two or more IG handles on key metrics and return a comparison summary.
from bloominsight.scraper import fetch_public_profile
from bloominsight.analyzer import analyze_profile

def compare_handles(handles: list[str]):
    results = {}
    for h in handles:
        try:
            p = fetch_public_profile(h)
            a = analyze_profile(p)
            results[h] = {"followers": a["followers"], "engagement_rate": a["engagement_rate"], "hashtag_count": a["hashtag_count"]}
        except Exception as e:
            results[h] = {"error": str(e)}
    # Simple leader summary
    leader = max([ (h, v) for h,v in results.items() if "error" not in v ], key=lambda x: x[1]["followers"], default=(None,{}))
    return {"results": results, "leader_by_followers": leader[0] if leader[0] else None}
