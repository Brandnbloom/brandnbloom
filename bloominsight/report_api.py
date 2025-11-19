# bloominsight/report_api.py
import os
from pathlib import Path
from db.models import save_report
from utils.pdf import make_report
from emailer.mailer import send_email

def generate_and_send_weekly_report(
    user_id: int,
    to_email: str,
    ig_handle: str,
    kpis: dict,
    logo_path: str = None
):
    """
    Generate a weekly PDF report for an Instagram handle and email it to the user.

    Parameters:
        user_id (int): ID of the user
        to_email (str): Recipient email address
        ig_handle (str): Instagram handle
        kpis (dict): Metrics & KPIs to include in report
        logo_path (str, optional): Path to brand logo for the report

    Returns:
        str: Path to the generated PDF
    """
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    pdf_path = reports_dir / f"{ig_handle}_weekly_report.pdf"

    action_plan = [
        "Double down on top 3 performing hashtags",
        "Increase Reels to 3x/week and track saves",
        "Refresh bio with crisp CTA + link",
        "Run A/B test on caption hooks for 2 weeks",
    ]

    # Generate the PDF report
    make_report(
        str(pdf_path),
        title=f"BloomInsight Weekly — @{ig_handle}",
        kpis=kpis,
        action_plan=action_plan,
        logo_path=logo_path
    )

    # Compose HTML email
    html = f"""
    <h3>Your BloomInsight Weekly Report — @{ig_handle}</h3>
    <p>Attached is your PDF report with key metrics and actionable recommendations.</p>
    """

    # Send email
    send_email(to_email, f"BloomInsight Weekly — @{ig_handle}", html, [str(pdf_path)])

    # Save report record in database
    save_report(user_id, ig_handle, str(pdf_path))

    return str(pdf_path)
