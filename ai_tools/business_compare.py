# ai_tools/business_compare.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import re


def analyze_site(url):
    score = 0
    insights = []

    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        load_time = time.time() - start
        soup = BeautifulSoup(response.text, "html.parser")

        # Reachable
        score += 20
        insights.append("✅ Website reachable")

        # HTTPS
        if url.startswith("https"):
            score += 10
            insights.append("✅ HTTPS enabled")
        else:
            insights.append("❌ HTTPS missing")

        # Meta title
        if soup.title and soup.title.string:
            score += 10
            insights.append("✅ Meta title present")
        else:
            insights.append("❌ Meta title missing")

        # Meta description
        if soup.find("meta", attrs={"name": "description"}):
            score += 10
            insights.append("✅ Meta description present")
        else:
            insights.append("❌ Meta description missing")

        # Page speed
        if load_time < 3:
            score += 20
            insights.append(f"✅ Fast load ({load_time:.2f}s)")
        else:
            insights.append(f"⚠️ Slow load ({load_time:.2f}s)")

        # Mobile friendly
        if soup.find("meta", attrs={"name": "viewport"}):
            score += 10
            insights.append("✅ Mobile optimized")
        else:
            insights.append("❌ Not mobile friendly")

        # Social links
        socials = re.findall(
            r"(instagram|linkedin|facebook|twitter)",
            response.text,
            re.I
        )
        if socials:
            score += 10
            insights.append("✅ Social presence detected")
        else:
            insights.append("❌ No social links found")

    except Exception as e:
        insights.append(f"❌ Error analyzing site: {e}")

    return score, insights


def run():
    st.markdown("## ⚖️ Business Compare")
    st.markdown("Compare your brand against competitors in real time.")

    col1, col2 = st.columns(2)

    with col1:
        site1 = st.text_input("Your Website (https://)")

    with col2:
        site2 = st.text_input("Competitor Website (https://)")

    if st.button("Compare Now"):
        if not site1 or not site2:
            st.warning("Please enter both websites")
            return

        with st.spinner("Analyzing websites..."):
            score1, insights1 = analyze_site(site1)
            score2, insights2 = analyze_site(site2)

        st.markdown("### 📊 Comparison Results")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"### 🌸 Your Brand")
            st.metric("Score", f"{score1}/100")
            for i in insights1:
                st.write(i)

        with c2:
            st.markdown(f"### 🧩 Competitor")
            st.metric("Score", f"{score2}/100")
            for i in insights2:
                st.write(i)

        st.markdown("---")

        if score1 > score2:
            st.success("🎉 Your brand is stronger than your competitor!")
        elif score2 > score1:
            st.warning("⚠️ Competitor brand is stronger. Improvement needed.")
        else:
            st.info("🤝 Both brands are equally strong.")
