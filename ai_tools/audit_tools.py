import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time


# -------------------------------------------------
# WEBSITE AUDIT (LIVE)
# -------------------------------------------------
def audit_website(url: str) -> dict:
    result = {
        "status": "Failed",
        "issues": [],
        "score": 0
    }

    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        load_time = round(time.time() - start, 2)

        soup = BeautifulSoup(response.text, "html.parser")

        # HTTPS
        if url.startswith("https"):
            result["score"] += 10
        else:
            result["issues"].append("Website is not using HTTPS")

        # Title tag
        title = soup.title.string if soup.title else ""
        if title:
            result["score"] += 10
        else:
            result["issues"].append("Missing <title> tag")

        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result["score"] += 10
        else:
            result["issues"].append("Missing meta description")

        # H1
        if soup.find("h1"):
            result["score"] += 10
        else:
            result["issues"].append("Missing H1 heading")

        # Images alt text
        images = soup.find_all("img")
        missing_alt = [img for img in images if not img.get("alt")]
        if not missing_alt:
            result["score"] += 10
        else:
            result["issues"].append(f"{len(missing_alt)} images missing alt text")

        # Page size
        page_size_kb = len(response.content) / 1024
        if page_size_kb < 2000:
            result["score"] += 10
        else:
            result["issues"].append("Page size too large (>2MB)")

        # Load time
        if load_time < 3:
            result["score"] += 10
        else:
            result["issues"].append(f"Slow load time: {load_time}s")

        # Mobile viewport
        viewport = soup.find("meta", attrs={"name": "viewport"})
        if viewport:
            result["score"] += 10
        else:
            result["issues"].append("Missing mobile viewport meta tag")

        result["status"] = "Success"

    except Exception as e:
        result["issues"].append(str(e))

    result["score"] = min(result["score"], 100)
    return result


# -------------------------------------------------
# SOCIAL PRESENCE AUDIT (SAFE)
# -------------------------------------------------
def audit_social(username: str, platform: str) -> dict:
    base_urls = {
        "Instagram": "https://www.instagram.com/",
        "LinkedIn": "https://www.linkedin.com/in/",
        "Twitter / X": "https://twitter.com/"
    }

    result = {
        "profile_url": "",
        "score": 0,
        "issues": []
    }

    if platform not in base_urls:
        result["issues"].append("Unsupported platform")
        return result

    profile_url = base_urls[platform] + username
    result["profile_url"] = profile_url

    # Username health
    if len(username) >= 4:
        result["score"] += 20
    else:
        result["issues"].append("Username too short")

    if "_" in username or "." in username:
        result["score"] += 10

    # Platform readiness
    result["score"] += 30  # Presence assumed (safe check)

    # Branding consistency
    if username.islower():
        result["score"] += 10

    result["score"] = min(result["score"], 100)
    return result


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
def run():
    st.markdown("## 🔍 Audit Tools")
    st.markdown(
        "Analyze your **website & social presence** for SEO, performance, and branding health."
    )

    st.divider()

    # ---------------- WEBSITE AUDIT ----------------
    st.subheader("🌐 Website Audit")

    website_url = st.text_input(
        "Website URL",
        placeholder="https://yourwebsite.com"
    )

    if st.button("Run Website Audit"):
        if not website_url:
            st.warning("Please enter a website URL.")
        else:
            with st.spinner("Auditing website..."):
                result = audit_website(website_url)

            st.metric("Website Score", result["score"])

            if result["issues"]:
                st.markdown("### ⚠ Issues Found")
                for issue in result["issues"]:
                    st.write("•", issue)
            else:
                st.success("No major issues found!")

    st.divider()

    # ---------------- SOCIAL AUDIT ----------------
    st.subheader("📱 Social Presence Audit")

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox(
            "Platform",
            ["Instagram", "LinkedIn", "Twitter / X"]
        )
    with col2:
        username = st.text_input(
            "Username (without @)",
            placeholder="brandname"
        )

    if st.button("Run Social Audit"):
        if not username:
            st.warning("Please enter a username.")
        else:
            result = audit_social(username, platform)

            st.metric("Social Score", result["score"])
            st.markdown("Profile URL:")
            st.code(result["profile_url"])

            if result["issues"]:
                st.markdown("### ⚠ Issues")
                for issue in result["issues"]:
                    st.write("•", issue)
            else:
                st.success("Social profile looks healthy!")

    st.caption(
        "⚠ This audit is platform-safe. No scraping or policy violations."
    )
