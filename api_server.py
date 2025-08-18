from fastapi import FastAPI
from bloominsight.report_api import generate_and_send_weekly_report

app = FastAPI(title="Brand N Bloom API")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/send-reports")
def send_reports():
    # TODO: query DB; demo payload
    user_id = 1
    email = "demo@example.com"
    handle = "brandnbloom_demo"
    kpis = {"Followers": 1500, "Likes": 360, "Reach": 900, "Impressions": 1800, "Engagement Rate (%)": 2.4}
    path = generate_and_send_weekly_report(user_id, email, handle, kpis)
    return {"status": "sent", "pdf": path}
