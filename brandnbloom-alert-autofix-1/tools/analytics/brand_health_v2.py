# brand_health_v2.py
# Refined brand health scoring with weighted components and fuzzy logo check (basic).
import math
from PIL import Image
import io
import requests

def score_bio(bio):
    if not bio or len(bio.strip()) < 20:
        return 0
    # looks for contact info or CTA words
    keywords = ['contact', 'email', 'www', 'link', 'shop', 'subscribe', 'book']
    score = 1
    for k in keywords:
        if k in bio.lower():
            score += 1
    return min(score, 3)

def score_profile_pic(url):
    if not url:
        return 0
    try:
        r = requests.get(url, timeout=8)
        img = Image.open(io.BytesIO(r.content))
        w,h = img.size
        # basic quality heuristics
        score = 0
        if w>=200 and h>=200:
            score += 1
        # aspect ratio near square
        if abs((w/h) - 1.0) < 0.3:
            score += 1
        # simplistic "face vs logo" check omitted — recommend manual review
        return min(score, 2)
    except Exception:
        return 0

def hashtag_variety(posts):
    tags = set()
    for p in posts:
        cap = p.get('caption') or ''
        for w in cap.split():
            if w.startswith('#'):
                tags.add(w.lower())
    if len(tags) >= 10:
        return 2
    elif len(tags) >=5:
        return 1
    return 0

def posting_frequency(posts):
    # posts is list with timestamp
    if not posts:
        return 0
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    recent = [p for p in posts if 'timestamp' in p and abs((now - pd_to_dt(p['timestamp'])).days) <= 30]
    if len(recent) >= 6:
        return 2
    elif len(recent) >= 3:
        return 1
    return 0

def pd_to_dt(ts):
    from datetime import datetime, timezone
    if isinstance(ts, str):
        return datetime.fromisoformat(ts.replace('Z','+00:00'))
    return ts

def compute_brand_health(profile, posts):
    # weights: bio 20%, pic 20%, hashtags 20%, frequency 20%, profile completeness 20%
    bio_s = score_bio(profile.get('biography',''))
    pic_s = score_profile_pic(profile.get('profile_pic_url'))
    tag_s = hashtag_variety(posts)
    freq_s = posting_frequency(posts)
    profile_complete = 1 if profile.get('followers') else 0
    raw = bio_s + pic_s + tag_s + freq_s + profile_complete
    max_raw = 3 + 2 + 2 + 2 + 1  # 10
    percent = int((raw / max_raw) * 100)
    return {'score': percent, 'components': {'bio':bio_s,'pic':pic_s,'hashtags':tag_s,'frequency':freq_s,'profile_complete':profile_complete}}
