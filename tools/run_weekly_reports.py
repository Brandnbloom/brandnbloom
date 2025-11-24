"""
Weekly Reports Runner

This script is designed to be used via cron, Render Scheduler, or GitHub Actions.

Enhancements:
- Iterates every active user from DB
- Per-user exception isolation
- Logs report activity
- Pulls KPIs with fallback logic
- Configurable defaults & paths
"""

import pathlib
import logging
from datetime import datetime

from db.models import get_kpis, get_all_users  # <-- UPDATED: must exist in your app
from bloominsight.report_api import generate_and_send_weekly_report


# -----------------------------
# CONFIGURATION
# -----------------------------

LOG_FILE = "logs/weekly_reports.log"
DEFAULT_LOGO_PATH = "assets/logo.png"
DEFAULT_KPIS = {
    "Followers": 1500,
    "Likes": 360,
    "Reach": 900,
    "Impressions": 1800,
    "Engagement Rate (%)": 2.4,
}
KPI_FETCH_LIMIT = 1  # Only need latest


# -----------------------------
# LOGGING SETUP
# -----------------------------

pathlib.Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("weekly_report")


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def get_logo_path():
    """Return logo path if exists, else None."""
    logo = pathlib.Path(DEFAULT_LOGO_PATH)
    return str(logo) if logo.exists() else None


def get_user_kpis(handle: str):
    """Fetch KPIs for user; fallback to defaults."""
    rows = get_kpis(handle, limit=KPI_FETCH_LIMIT) or []
    if not rows:
        logger.warning(f"No KPIs found for {handle}, using defaults.")
        return DEFAULT_KPIS

    row = rows[0]
    return {
        "Followers": row.get("followers", DEFAULT_KPIS["Followers"]),
        "Likes": row.get("likes", DEFAULT_KPIS["Likes"]),
        "Reach": row.get("reach", DEFAULT_KPIS["Reach"]),
        "Impressions": row.get("impressions", DEFAULT_KPIS["Impressions"]),
        "Engagement Rate (%)": row.get("engagement_rate", DEFAULT_KPIS["Engagement Rate (%)"]),
    }


# -----------------------------
# MAIN LOGIC
# -----------------------------

def run_for_all_users():
    """Generate and email weekly reports for all users."""

    logger.info("=== Weekly Report Job Started ===")

    try:
        users = get_all_users()
    except Exception as e:
        logger.error(f"Failed to load users: {e}")
        return

    if not users:
        logger.warning("No users found. Job finished with no action.")
        return

    logo_path = get_logo_path()

    for u in users:
        user_id = u.id
        email = u.email
        handle = u.handle

        logger.info(f"Processing user: {handle} ({email})")

        try:
            # KPI extraction
            kpis = get_user_kpis(handle)

            # Generate & send report
            pdf = generate_and_send_weekly_report(
                user_id=user_id,
                email=email,
                handle=handle,
                kpis=kpis,
                logo_path=logo_path,
            )

            logger.info(f"Report sent to {email} | PDF: {pdf}")

        except Exception as e:
            logger.error(f"Error generating report for {handle}: {e}")

    logger.info("=== Weekly Report Job Completed ===")


if __name__ == "__main__":
    run_for_all_users()
