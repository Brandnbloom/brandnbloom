from bloominsight.analyzer import analyze_profile
from bloominsight.utils import engagement_rate
import math

def compute_bloomscore(profile: dict) -> dict:
    analysis = analyze_profile(profile)
    # Components: ER (40), posting consistency (20), hashtag variety (15), bio+logo (15), growth (10)
    er = analysis.get("engagement_rate", 0)  # 0-100
    posting = 20 if analysis.get("hashtag_count",0) >= 3 else 10
    hashtag_var = 15 if analysis.get("hashtag_count",0) >= 5 else 7
    bio_logo = 15 if analysis.get("brand_health_score",0) >= 50 else 8
    growth = 10  # placeholder: could calculate avg growth
    score = min(100, int(er*0.4 + posting + hashtag_var + bio_logo + growth))
    buckets = "Excellent" if score>=80 else "Good" if score>=60 else "Fair" if score>=40 else "Needs Work"
    return {"score": score, "bucket": buckets, "components": {"er": er, "posting": posting, "hashtag_variety": hashtag_var, "bio_logo": bio_logo, "growth": growth}, "analysis": analysis}
