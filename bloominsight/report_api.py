import os
from pathlib import Path
from db.models import save_report
from utils.pdf import make_report
from emailer.mailer import send_email

def generate_and_send_weekly_report(user_id: int, to_email: str, ig_handle: str, kpis: dict, logo_path: str = None):
    reports_dir = Path("reports"); reports_dir.mkdir(exist_ok=True)
    pdf_path = str(reports_dir / f"{ig_handle}_weekly_report.pdf")

    action_plan = [
        "Double down on top 3 performing hashtags",
        "Increase Reels to 3x/week and track saves",
        "Refresh bio with crisp CTA + link",
        "Run A/B test on caption hooks for 2 weeks",
    ]

    make_report(pdf_path, f"BloomInsight Weekly — @{ig_handle}", kpis, action_plan, logo_path=logo_path)
    html = f"""
    <h3>Your BloomInsight Weekly Report — @{ig_handle}</h3>
    <p>Attached is your PDF report with metrics and an action plan.</p>
    """
    send_email(to_email, f"BloomInsight Weekly — @{ig_handle}", html, [pdf_path])
    save_report(user_id, ig_handle, pdf_path)
    return pdf_path
