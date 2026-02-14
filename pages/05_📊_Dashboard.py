import streamlit as st
import pandas as pd
from datetime import datetime
from auth.session import require_login, get_user
from bloominsight.scraper import fetch_public_profile
from bloominsight.analyzer import analyze_profile
from db.models import log_kpis, get_kpis
from utils.charts import kpi_line
from bloominsight.report_api import generate_and_send_weekly_report
from utils.ui import inject_css, dark_mode_toggle

st.title("📊 Dashboard")
inject_css(); dark_mode_toggle()
require_login()
user = get_user()

st.caption("Track KPIs, log history, and email weekly PDF reports — all in one place.")

handle = st.text_input("Instagram Handle (without @)", value="brandnbloom_demo")
colA, colB = st.columns([1,1])
with colA:
    if st.button("Fetch & Analyze"):
        profile = fetch_public_profile(handle)
        analysis = analyze_profile(profile)
        log_kpis(handle, analysis["followers"], analysis["likes"], analysis["reach"], analysis["impressions"], analysis["engagement_rate"])
        st.session_state["last_analysis"] = analysis
        st.success("Profile analyzed and KPIs logged.")
with colB:
    if st.button("Send Weekly PDF Now"):
        analysis = st.session_state.get("last_analysis") or {}
        if not analysis:
            st.warning("Analyze first to generate KPIs.")
        else:
            kpis = {
                "Followers": analysis["followers"],
                "Likes": analysis["likes"],
                "Reach": analysis["reach"],
                "Impressions": analysis["impressions"],
                "Engagement Rate (%)": analysis["engagement_rate"],
            }
            import pathlib
            logo = pathlib.Path('assets/logo.png') if pathlib.Path('assets/logo.png').exists() else None
            pdf = generate_and_send_weekly_report(user["id"], user["email"], handle, kpis, logo_path=str(logo) if logo else None)
            st.success(f"Report emailed! Saved at: {pdf}")

st.divider()

rows = get_kpis(handle, limit=100)
df = pd.DataFrame(rows, columns=rows[0].keys()) if rows else pd.DataFrame(columns=["timestamp","followers","likes","reach","impressions","engagement_rate"])

if df.empty:
    st.info("No KPI data yet. Click **Fetch & Analyze** to begin.")
else:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Followers", int(df.iloc[0]["followers"]))
    c2.metric("Likes", int(df.iloc[0]["likes"]))
    c3.metric("Reach", int(df.iloc[0]["reach"]))
    c4.metric("Impressions", int(df.iloc[0]["impressions"]))
    c5.metric("ER (%)", float(df.iloc[0]["engagement_rate"]))

    for y, title in [
        ("followers", "Followers Over Time"),
        ("likes", "Likes Over Time"),
        ("reach", "Reach Over Time"),
        ("impressions", "Impressions Over Time"),
        ("engagement_rate", "Engagement Rate (%) Over Time"),
    ]:
        fig = kpi_line(df.copy(), y=y, title=title)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
