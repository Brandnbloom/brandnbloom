# ai_tools/audit_tools.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def run():
    st.markdown("## 🔍 Website Audit Tool")
    st.markdown("Analyze your website’s technical, SEO, and brand health.")

    url = st.text_input("Enter your website URL", placeholder="https://example.com")

    if not url:
        st.info("Please enter a website URL to begin.")
        return

    if not url.startswith("http"):
        st.error("Please include http:// or https://")
        return

    if st.button("Run Audit"):
        with st.spinner("Auditing website..."):
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")

                results = {}

                # ------------------------
                # Technical checks
                # ------------------------
                results["HTTPS"] = "✅ Secure" if url.startswith("https") else "❌ Not Secure"
                results["Status Code"] = response.status_code

                # ------------------------
                # SEO checks
                # ------------------------
                title = soup.title.string.strip() if soup.title else None
                meta_desc = soup.find("meta", attrs={"name": "description"})
                h1 = soup.find("h1")

                results["Title Tag"] = title if title else "❌ Missing"
                results["Meta Description"] = (
                    meta_desc["content"] if meta_desc and meta_desc.get("content") else "❌ Missing"
                )
                results["H1 Tag"] = h1.text.strip() if h1 else "❌ Missing"

                # ------------------------
                # Brand / UX checks
                # ------------------------
                text = soup.get_text().lower()
                cta_keywords = ["buy", "contact", "signup", "subscribe", "book"]
                results["CTA Detected"] = (
                    "✅ Yes" if any(k in text for k in cta_keywords) else "❌ No clear CTA"
                )

                # ------------------------
                # Display results
                # ------------------------
                st.success("Audit completed successfully")

                st.markdown("### 🛠 Technical")
                st.write("HTTPS:", results["HTTPS"])
                st.write("Status Code:", results["Status Code"])

                st.markdown("### 🔎 SEO")
                st.write("Title Tag:", results["Title Tag"])
                st.write("Meta Description:", results["Meta Description"])
                st.write("H1 Tag:", results["H1 Tag"])

                st.markdown("### 🎯 Brand & UX")
                st.write("CTA:", results["CTA Detected"])

            except Exception as e:
                st.error("Audit failed. Please try again.")
                st.exception(e)
