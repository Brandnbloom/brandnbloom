ai_tools/audit_tools.py

import streamlit as st 
import requests 
from bs4 import BeautifulSoup 
from urllib.parse import urlparse

def run(): 
    st.markdown("### 🔍 Website Audit (Live)") 
    st.caption("Real-time technical & content audit — no mock data")
    url = st.text_input("Enter website URL", placeholder="https://example.com")

if not url:
    return

if not url.startswith("http"):
    st.error("Please enter a valid URL including http:// or https://")
    return

with st.spinner("Auditing website…"):
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "BrandNBloomAuditBot"})
        load_time = response.elapsed.total_seconds()
        status_code = response.status_code

        soup = BeautifulSoup(response.text, "html.parser")

        # ---------------- BASIC CHECKS ----------------
        title = soup.title.string.strip() if soup.title else None
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc["content"].strip() if meta_desc else None

        h1_tags = soup.find_all("h1")
        img_tags = soup.find_all("img")
        imgs_without_alt = [img for img in img_tags if not img.get("alt")]

        links = soup.find_all("a", href=True)
        internal_links = 0
        external_links = 0

        domain = urlparse(url).netloc
        for link in links:
            href = link.get("href")
            if domain in href:
                internal_links += 1
            elif href.startswith("http"):
                external_links += 1

        # ---------------- RESULTS ----------------
        st.success("Audit completed")

        c1, c2, c3 = st.columns(3)
        c1.metric("Status Code", status_code)
        c2.metric("Load Time (sec)", round(load_time, 2))
        c3.metric("Page Title", "OK" if title else "Missing")

        st.markdown("---")

        st.markdown("#### 🧠 SEO & Content")
        st.write("**Title:**", title or "❌ Missing")
        st.write("**Meta Description:**", meta_desc or "❌ Missing")
        st.write("**H1 Tags:**", len(h1_tags))

        st.markdown("#### 🖼 Accessibility")
        st.write("Total Images:", len(img_tags))
        st.write("Images Missing ALT:", len(imgs_without_alt))

        st.markdown("#### 🔗 Links")
        st.write("Internal Links:", internal_links)
        st.write("External Links:", external_links)

        # ---------------- SIMPLE SCORE ----------------
        score = 100
        if not title:
            score -= 15
        if not meta_desc:
            score -= 15
        if len(h1_tags) != 1:
            score -= 10
        if imgs_without_alt:
            score -= min(20, len(imgs_without_alt))
        if load_time > 3:
            score -= 10

        score = max(score, 0)

        st.markdown("---")
        st.markdown(f"## 🌸 Bloom Audit Score: **{score}/100**")

        if score >= 80:
            st.success("Great foundation! Minor optimizations needed.")
        elif score >= 50:
            st.warning("Average performance. SEO & UX improvements recommended.")
        else:
            st.error("Poor performance. Immediate fixes required.")

    except Exception as e:
        st.error("Audit failed. The site may block bots or be unreachable.")
        st.exception(e)
