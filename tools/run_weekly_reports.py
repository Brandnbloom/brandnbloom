# This script can be invoked by a Render Cron Job.
# It generates & emails weekly reports for each user/handle (demo flow).
from db.models import get_kpis
from bloominsight.report_api import generate_and_send_weekly_report

# TODO: iterate all users/handles from DB. For demo, single handle:
user_id = 1
email = "demo@example.com"
handle = "brandnbloom_demo"

rows = get_kpis(handle, limit=1) or []
if rows:
    row = rows[0]
    kpis = {
        "Followers": row["followers"],
        "Likes": row["likes"],
        "Reach": row["reach"],
        "Impressions": row["impressions"],
        "Engagement Rate (%)": row["engagement_rate"],
    }
else:
    kpis = {"Followers": 1500, "Likes": 360, "Reach": 900, "Impressions": 1800, "Engagement Rate (%)": 2.4}

import pathlib
logo = pathlib.Path('assets/logo.png') if pathlib.Path('assets/logo.png').exists() else None
pdf = generate_and_send_weekly_report(user_id, email, handle, kpis, logo_path=str(logo) if logo else None)
print("Report generated & sent:", pdf)
