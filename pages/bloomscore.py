import streamlit as st
import requests, random, io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils import can_use_tool, increment_usage

# 1️⃣ Enforce usage limit
user_email = st.experimental_user.email if st.experimental_user else "guest@example.com"
allowed, remaining = can_use_tool(user_email)
if not allowed:
    st.warning("You've used all 3 free tries! Please upgrade to continue.")
    st.markdown("👉 [Upgrade via PayPal — $5/month or $50/year]")
    st.stop()

st.title("🌟 BloomScore — Real-Time Brand Health Check")

# 2️⃣ Collect user input
insta_link = st.text_input("Instagram Profile Link (e.g., https://www.instagram.com/yourrestaurant)")
website_url = st.text_input("Website URL (e.g., https://yourrestaurant.com)")
if st.button("🔍 Generate BloomScore"):
    increment_usage(user_email)

    # 3️⃣ Get Instagram data via Graph API
    insta_stats = {}
    try:
        token = st.secrets["IG_ACCESS_TOKEN"]
        user_id = st.secrets["IG_USER_ID"]
        url = f"https://graph.facebook.com/v17.0/{user_id}?fields=followers_count,media_count&access_token={token}"
        resp = requests.get(url).json()
        insta_stats = {
            "followers": resp.get("followers_count", 0),
            "posts": resp.get("media_count", 0)
        }
    except:
        insta_stats = {"followers": 0, "posts": 0}

    # 4️⃣ Website performance via PageSpeed Insights
    psi_stats = {}
    try:
        psi_key = st.secrets["PAGESPEED_KEY"]
        psi_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={website_url}&key={psi_key}"
        resp2 = requests.get(psi_url).json()
        labs = resp2["lighthouseResult"]["audits"]
        psi_stats = {
            "LCP": labs["largest-contentful-paint"]["displayValue"],
            "FCP": labs["first-contentful-paint"]["displayValue"],
            "CLS": labs["cumulative-layout-shift"]["displayValue"]
        }
    except:
        psi_stats = {"LCP": "N/A", "FCP": "N/A", "CLS": "N/A"}

    # 5️⃣ Compute BloomScore (simple algorithm)
    score = (min(insta_stats["followers"]/100, 30) +
             min(insta_stats["posts"]/10, 30) +
             (30 if psi_stats["LCP"]!="N/A" else 0)) / 90 * 100
    st.success(f"🎯 Your BloomScore: *{int(score)}/100*")

    # 6️⃣ Show metrics
    st.subheader("📊 Instagram Metrics")
    st.write(insta_stats)
    st.subheader("🌐 PageSpeed Metrics")
    st.write(psi_stats)

    # 7️⃣ Generate downloadable PDF
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(50, 750, "🌟 BloomScore Report")
    pdf.drawString(50, 720, f"Instagram Followers: {insta_stats['followers']}")
    pdf.drawString(50, 700, f"Instagram Posts: {insta_stats['posts']}")
    pdf.drawString(50, 680, f"LCP: {psi_stats['LCP']}, FCP: {psi_stats['FCP']}, CLS: {psi_stats['CLS']}")
    pdf.drawString(50, 650, f"Final Score: {int(score)}/100")
    pdf.save()
    buffer.seek(0)
    st.download_button("📥 Download PDF Report", buffer, file_name="BloomScore_Report.pdf", mime="application/pdf")


---

🔧 What to Do Next

1. Add your IG_ACCESS_TOKEN, IG_USER_ID, and PAGESPEED_KEY in Streamlit Secrets:

IG_ACCESS_TOKEN = "your_instagram_graph_token"
IG_USER_ID = "your_fb_ig_user_id"
PAGESPEED_KEY = "your_google_pagespeed_api_key"
