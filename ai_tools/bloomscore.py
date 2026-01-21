# ai_tools/bloomscore.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import re


def run():
    st.markdown("## 🌸 BloomScore")
    st.markdown("Instant brand health score for your website")

    url = st.text_input("Enter website URL (with https://)")

    if st.button("Calculate BloomScore"):
        if not url.startswith("http"):
            st.error("Please enter a valid URL starting with http or https")
            return

        score = 0
        details = []

        try:
            start = time.time()
            response = requests.get(url, timeout=10)
            load_time = time.time() - start
            soup = BeautifulSoup(response.text, "html.parser")

            # 1️⃣ Site reachable
            score += 20
            details.append("✅ Website reachable")

            # 2️⃣ HTTPS
            if url.startswith("https"):
                score += 10
                details.append("✅ HTTPS enabled")
            else:
                details.append("❌ No HTTPS")

            # 3️⃣ Meta title
            if soup.title and soup.title.string:
                score += 10
                details.append("✅ Meta title found")
            else:
                details.append("❌ Missing meta title")

            # 4️⃣ Meta description
            if soup.find("meta", attrs={"name": "description"}):
                score += 10
                details.append("✅ Meta description found")
            else:
                details.append("❌ Missing meta description")

            # 5️⃣ Page speed
            if load_time < 3:
                score += 20
                details.append(f"✅ Fast load time ({load_time:.2f}s)")
            else:
                details.append(f"⚠️ Slow load time ({load_time:.2f}s)")

            # 6️⃣ Mobile viewport
            if soup.find("meta", attrs={"name": "viewport"}):
                score += 10
                details.append("✅ Mobile friendly")
            else:
                details.append("❌ Not mobile optimized")

            # 7️⃣ Social links
            socials = re.findall(r"(instagram|linkedin|facebook|twitter)", response.text, re.I)
            if socials:
                score += 10
                details.append("✅ Social links detected")
            else:
                details.append("❌ No social links found")

            # 8️⃣ Image alt tags
            images = soup.find_all("img")
            if images and all(img.get("alt") for img in images[:5]):
                score += 10
                details.append("✅ Image alt tags present")
            else:
                details.append("⚠️ Missing image alt tags")

            # 🎯 Final Output
            st.markdown(f"### 🌼 BloomScore: **{score}/100**")

            for d in details:
                st.write(d)

            if score >= 80:
                st.success("Excellent brand health 🚀")
            elif score >= 50:
                st.warning("Good, but needs improvement 🌱")
            else:
                st.error("Brand health needs urgent attention ⚠️")

        except Exception as e:
            st.error("Failed to analyze website")
            st.exception(e)
