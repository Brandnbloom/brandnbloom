# brandnbloom/bloomscore_pro_v2.py

from typing import Dict, List
import os, tempfile
import math
import numpy as np
import json
from brandnbloom.report_generator import render_html_report, export_pdf_from_html

# -----------------------------
# Load Branding
# -----------------------------
BRANDING_PATH = os.path.join(os.path.dirname(__file__), "branding.json")
with open(BRANDING_PATH, "r", encoding="utf-8") as f:
    BRANDING = json.load(f)

# -----------------------------
# Benchmarking Data & Helpers
# -----------------------------
DEFAULT_INDUSTY_AVERAGES = {
    "beauty": 65,
    "food": 58,
    "tech": 62,
    "fashion": 68,
    "default": 60
}

IDEAL_BY_ACCOUNT_TYPE = {
    "personal_brand": 75,
    "corporate": 70,
    "small_business": 65,
    "creator": 72
}

def clean_competitors(scores: List[float]) -> List[float]:
    cleaned = []
    for s in scores:
        try:
            if s is None: continue
            s = float(s)
            if np.isnan(s) or np.isinf(s) or s < 0: continue
            cleaned.append(s)
        except Exception:
            continue
    return cleaned

def compare_to_competitors(score: float, competitor_scores: List[float]) -> Dict:
    competitors = clean_competitors(competitor_scores)
    if not competitors:
        return {
            "percentile_vs_competitors": None,
            "avg_competitor_score": None,
            "recommendation": "Insufficient competitor data"
        }
    arr = np.array(competitors)
    percentile = int((arr < score).sum() / len(arr) * 100)
    mean_comp = float(arr.mean())
    return {
        "percentile_vs_competitors": percentile,
        "avg_competitor_score": round(mean_comp, 2),
        "recommendation": "Above competitors" if score > mean_comp else "Below competitors"
    }

def compare_to_industry(score: float, industry: str = "default") -> Dict:
    avg = DEFAULT_INDUSTY_AVERAGES.get(industry, DEFAULT_INDUSTY_AVERAGES["default"])
    delta = score - avg
    return {
        "industry_average": avg,
        "difference": round(delta, 2),
        "status": "Above average" if delta > 0 else "Below average" if delta < 0 else "At average"
    }

def compare_to_ideal(score: float, account_type: str = "personal_brand") -> Dict:
    ideal = IDEAL_BY_ACCOUNT_TYPE.get(account_type, IDEAL_BY_ACCOUNT_TYPE["personal_brand"])
    delta = score - ideal
    return {
        "ideal_score": ideal,
        "difference": round(delta, 2),
        "status": "Meets or exceeds ideal" if delta >= 0 else "Below ideal"
    }

# -----------------------------
# BloomScore Engine
# -----------------------------
def _score_profile_aesthetics(image_bytes: bytes, brand_palette: List[str] = None) -> float:
    from brandnbloom.ai_tools.color_extractor import extract_dominant_colors
    from brandnbloom.ai_tools.utils import palette_luminance

    try:
        palette = extract_dominant_colors(image_bytes, num_colors=5)
    except Exception:
        palette = brand_palette or ["#A25A3C", "#F7F1EB", "#3C2F2F"]

    lum = palette_luminance(palette)
    lum_score = max(0, min(100, (lum / 255) * 120))
    
    brand_align = 100.0
    if brand_palette:
        def dist(a, b): return sum((x-y)**2 for x,y in zip(a,b))**0.5
        bp_rgb = [tuple(int(b.lstrip("#")[i:i+2], 16) for i in (0,2,4)) for b in brand_palette]
        pal_rgb = [tuple(int(p.lstrip("#")[i:i+2], 16) for i in (0,2,4)) for p in palette]
        dists = [min(dist(p, b) for b in bp_rgb) for p in pal_rgb]
        avgd = float(np.mean(dists)) if dists else 100
        brand_align = max(0, min(100, 100 - (avgd/200)*100))
    
    return (0.6 * lum_score) + (0.4 * brand_align)

def _score_content_language_tone(sample_texts: List[str]) -> float:
    if not sample_texts: return 50.0
    from brandnbloom.ai_tools.ocr_sentiment import sentiment_of_text
    scores = []
    for t in sample_texts:
        s = sentiment_of_text(t)
        scores.append((s.get("polarity", 0) + 1) * 50)
    return float(sum(scores) / len(scores))

def _score_reels_posts_mix(metrics: Dict) -> float:
    r = metrics.get("reels_ratio", None)
    if r is None: return 50.0
    optimal = 0.4
    score = max(0, 1 - abs(r - optimal) / 0.5)
    return score * 100

def _score_save_share(metrics: Dict) -> float:
    saves = metrics.get("saves_per_post", 0)
    shares = metrics.get("shares_per_post", 0)
    s_score = min(100, (saves / 20) * 100)
    sh_score = min(100, (shares / 10) * 100)
    return (0.6 * s_score) + (0.4 * sh_score)

def _score_reach_quality(metrics: Dict) -> float:
    reach = metrics.get("reach", 0)
    followers = max(1, metrics.get("followers", 1))
    engaged = max(0, metrics.get("engaged_unique", 0))
    rr = min(2.0, reach / followers)
    engaged_ratio = min(1.0, engaged / (reach + 1e-6))
    return (rr * 50 + engaged_ratio * 50)

def _score_story_consistency(metrics: Dict) -> float:
    spw = metrics.get("stories_per_week", 0)
    interactions = metrics.get("sticker_interactions_per_week", 0)
    freq_score = min(100, (spw / 7) * 100)
    int_score = min(100, (interactions / 20) * 100)
    return 0.6 * freq_score + 0.4 * int_score

def compute_bloomscore_v2(profile: Dict) -> Dict:
    img = profile.get("image_bytes", None)
    texts = profile.get("sample_texts", [])
    metrics = profile.get("metrics", {})
    brand_palette = profile.get("brand_palette", None)

    weights = {
        "aesthetics": 0.20,
        "language_tone": 0.15,
        "reels_posts_mix": 0.15,
        "save_share": 0.20,
        "reach_quality": 0.15,
        "story_consistency": 0.15
    }

    aesthetics_score = _score_profile_aesthetics(img, brand_palette) if img else 50.0
    language_score = _score_content_language_tone(texts)
    reels_posts_score = _score_reels_posts_mix(metrics)
    save_share_score = _score_save_share(metrics)
    reach_quality_score = _score_reach_quality(metrics)
    story_score = _score_story_consistency(metrics)

    total = (
        weights["aesthetics"] * aesthetics_score +
        weights["language_tone"] * language_score +
        weights["reels_posts_mix"] * reels_posts_score +
        weights["save_share"] * save_share_score +
        weights["reach_quality"] * reach_quality_score +
        weights["story_consistency"] * story_score
    )

    final_score = max(0, min(100, round(total, 2)))

    return {
        "final_score": final_score,
        "components": {
            "aesthetics": round(aesthetics_score, 2),
            "language_tone": round(language_score, 2),
            "reels_posts_mix": round(reels_posts_score, 2),
            "save_share": round(save_share_score, 2),
            "reach_quality": round(reach_quality_score, 2),
            "story_consistency": round(story_score, 2),
        },
        "weights": weights,
        "raw_metrics": metrics
    }

# -----------------------------
# Full Report Generation
# -----------------------------
def generate_full_report(profile: dict, competitors: list = None, industry: str = "default", account_type: str = "personal_brand"):
    result = compute_bloomscore_v2(profile)
    score = result["final_score"]

    bench_comp = compare_to_competitors(score, competitors or [])
    bench_ind = compare_to_industry(score, industry)
    bench_ideal = compare_to_ideal(score, account_type)

    bucket = "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair" if score >= 40 else "Needs Work"

    payload = {
        "score": score,
        "bucket": bucket,
        "components": result["components"],
        "palette": profile.get("brand_palette", list(BRANDING["palette"].values())),
        "fonts": BRANDING.get("fonts", {}),
        "benchmark": {
            "industry_average": bench_ind["industry_average"],
            "avg_competitor_score": bench_comp.get("avg_competitor_score"),
            "ideal_score": bench_ideal["ideal_score"],
            "status": bench_ideal["status"]
        },
        "pricing": BRANDING.get("pricing", [])
    }

    html = render_html_report(payload)

    pdf_path = None
    try:
        tmp = tempfile.gettempdir()
        out = os.path.join(tmp, f"bloom_report_{score}.pdf")
        export_pdf_from_html(html, out)
        pdf_path = out
    except Exception:
        pdf_path = None

    return {"html": html, "pdf_path": pdf_path, "payload": payload}
