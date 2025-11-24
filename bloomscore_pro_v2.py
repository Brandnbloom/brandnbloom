# brandnbloom/bloomscore_pro_v2.py

import os
import tempfile
import numpy as np
from brandnbloom.bloom_engine import compute_bloomscore_v2
from brandnbloom.benchmarking import compare_to_competitors, compare_to_industry, compare_to_ideal
from brandnbloom.report_generator import render_html_report, export_pdf_from_html

def generate_full_report(profile: dict, competitors: list = None, industry: str = "default", account_type: str = "personal_brand"):
    """
    Generate full BloomScore Pro v2 report including benchmarking, HTML preview, and optional PDF.

    Args:
        profile (dict): User profile with image and sample texts.
        competitors (list, optional): List of competitor scores.
        industry (str, optional): Industry type for benchmarking.
        account_type (str, optional): Account type for ideal score benchmarking.

    Returns:
        dict: {
            "html": HTML preview of report,
            "pdf_path": Path to PDF file (or None),
            "payload": Full report data including score, bucket, components, palette, and benchmarks
        }
    """

    # 1) Compute BloomScore
    result = compute_bloomscore_v2(profile)
    score = result.get("final_score", 0)
    components = result.get("components", {})

    # 2) Benchmarking
    competitors = competitors or []
    bench_comp = compare_to_competitors(score, competitors)
    bench_ind = compare_to_industry(score, industry)
    bench_ideal = compare_to_ideal(score, account_type)

    # 3) Compute Z-score vs competitors (if enough data)
    z_score = None
    comp_clean = [c for c in competitors if isinstance(c, (int, float))]
    if len(comp_clean) > 1:
        z_score = round((score - np.mean(comp_clean)) / np.std(comp_clean), 2)

    # 4) Determine bucket
    bucket = (
        "Excellent" if score >= 80 else
        "Good" if score >= 60 else
        "Fair" if score >= 40 else
        "Needs Work"
    )

    # 5) Build payload
    payload = {
        "score": score,
        "bucket": bucket,
        "components": components,
        "palette": profile.get("brand_palette") or ["#A25A3C", "#F7F1EB", "#3C2F2F"],
        "benchmark": {
            "industry_average": bench_ind.get("industry_average"),
            "industry_status": bench_ind.get("status"),
            "avg_competitor_score": bench_comp.get("avg_competitor_score"),
            "competitor_percentile": bench_comp.get("percentile_vs_competitors"),
            "competitor_recommendation": bench_comp.get("recommendation"),
            "ideal_score": bench_ideal.get("ideal_score"),
            "ideal_status": bench_ideal.get("status"),
            "z_score_vs_competitors": z_score
        }
    }

    # 6) Render HTML
    html = render_html_report(payload)

    # 7) Export PDF safely
    pdf_path = None
    try:
        tmp_dir = tempfile.gettempdir()
        safe_score = str(score).replace(".", "_")
        out_file = os.path.join(tmp_dir, f"bloom_report_{safe_score}.pdf")
        export_pdf_from_html(html, out_file)
        pdf_path = out_file if os.path.exists(out_file) else None
    except Exception:
        pdf_path = None  # Ensure HTML still returns even if PDF fails

    return {"html": html, "pdf_path": pdf_path, "payload": payload}
