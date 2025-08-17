from collections import Counter
import pandas as pd
import math
from datetime import datetime
from nlp_utils import summarize_caption, suggest_hashtags

def analyze_posts(profile, posts):
    # posts: list of dicts
    if not posts:
        return {}
    df = pd.DataFrame(posts)
    total_likes = int(df['likes'].sum())
    total_comments = int(df['comments'].sum())
    avg_likes = float(df['likes'].mean())
    avg_comments = float(df['comments'].mean())
    engagement_rate = compute_engagement_rate(avg_likes, avg_comments, profile.get('followers',1))
    hashtags = Counter()
    caption_summaries = []
    for c in df['caption'].fillna(""):
        caption_summaries.append(summarize_caption(c))
        for tag in suggest_hashtags(c, top_n=5):
            hashtags[tag]+=1
    kpis = {
        "total_posts_analyzed": len(df),
        "total_likes": total_likes,
        "total_comments": total_comments,
        "avg_likes": avg_likes,
        "avg_comments": avg_comments,
        "engagement_rate_percent": round(engagement_rate*100,2),
        "top_hashtags": hashtags.most_common(10),
        "caption_summaries": caption_summaries
    }
    return kpis

def compute_engagement_rate(avg_likes, avg_comments, followers):
    try:
        followers = max(1,int(followers))
        return (avg_likes + avg_comments) / followers
    except Exception:
        return 0.0

def compute_brand_health(profile, posts):
    """
    Brand health percent based on simple heuristics:
    - biography completeness
    - profile picture presence
    - posting frequency (recent 30 days)
    - hashtag variety
    """
    score = 0
    max_score = 4
    # bio completeness
    bio = profile.get('biography') or ""
    if len(bio.strip())>20:
        score+=1
    # profile pic
    if profile.get('profile_pic_url'):
        score+=1
    # posting frequency
    timestamps = [p.get('timestamp') for p in posts if p.get('timestamp')]
    if timestamps:
        now = datetime.utcnow().timestamp()
        # count posts in last 30 days
        recent = [t for t in timestamps if (now - t) < (30*24*3600)]
        if len(recent)>=3:
            score+=1
    # hashtag variety (from captions)
    hashtags = set()
    for p in posts:
        caps = p.get('caption') or ""
        for w in caps.split():
            if w.startswith("#"):
                hashtags.add(w.lower())
    if len(hashtags) >= 5:
        score+=1
    percent = int((score/max_score)*100)
    return {"score":percent, "components":{"bio":len(bio.strip())>20,"profile_pic":bool(profile.get('profile_pic_url')),"posting_freq":len(timestamps)>0,"hashtag_variety":len(hashtags)}}
