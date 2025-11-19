# brandnbloom/bloomscore_pro_v2.py
from brandnbloom.bloom_engine import compute_bloomscore_v2
from brandnbloom.benchmarking import compare_to_competitors, compare_to_industry, compare_to_ideal
from brandnbloom.report_generator import render_html_report, export_pdf_from_html

def generate_full_report(profile: dict, competitors: list = None, industry: str = "default", account_type: str = "personal_brand"):
    # 1) compute score
    result = compute_bloomscore_v2(profile)
    score = result["final_score"]

    # 2) benchmarking
    bench_comp = compare_to_competitors(score, competitors or [])
    bench_ind = compare_to_industry(score, industry)
    bench_ideal = compare_to_ideal(score, account_type)

    # 3) bucket
    bucket = "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair" if score >= 40 else "Needs Work"

    payload = {
        "score": score,
        "bucket": bucket,
        "components": result["components"],
        "palette": profile.get("brand_palette", ["#A25A3C", "#F7F1EB", "#3C2F2F"]),
        "benchmark": {
            "industry_average": bench_ind["industry_average"],
            "avg_competitor_score": bench_comp.get("avg_competitor_score"),
            "ideal_score": bench_ideal["ideal_score"],
            "status": bench_ideal["status"]
        }
    }

    html = render_html_report(payload)

    # optionally export pdf
    pdf_path = None
    try:
        import os, tempfile
        tmp = tempfile.gettempdir()
        out = os.path.join(tmp, f"bloom_report_{score}.pdf")
        export_pdf_from_html(html, out)
        pdf_path = out
    except Exception:
        pdf_path = None  # we still return HTML

    return {"html": html, "pdf_path": pdf_path, "payload": payload}
