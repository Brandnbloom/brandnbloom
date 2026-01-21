import streamlit as st
import requests
from bs4 import BeautifulSoup
import time


# -------------------------------------------------
# WEBSITE ANALYSIS ENGINE
# -------------------------------------------------
def analyze_site(url: str) -> dict:
    score = 0
    issues = []

    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        load_time = round(time.time() - start, 2)

        soup = BeautifulSoup(response.text, "html.parser")

        # HTTPS
        if url.startswith("https"):
            score += 10
        else:
            issues.append("No HTTPS")

        # Title
        if soup.title and soup.title.string:
            score += 10
        else:
            issues.append("Missing title tag")

        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            score += 10
        else:
            issues.append("Missing meta description")

        # H1
        if soup.find("h1"):
            score += 10
        else:
            issues.append("Missing H1 heading")

        # Images alt text
        images = soup.find_all("img")
        if images:
            missing_alt = [img for img in images if not img.get("alt")]
            if not missing_alt:
                score += 10
            else:
                issues.append(f"{len(missing_alt)} images missing alt text")
        else:
            score += 5  # no images, no penalty

        # Load time
        if load_time < 3:
            score += 10
        else:
            issues.append(f"Slow load time ({load_time}s)")

        # Page size
        page_size_kb = len(response.content) / 1024
        if page_size_kb < 2000:
            score += 10
        else:
            issues.append("Page size too large")

        # Mobile viewport
        if soup.find("meta", attrs={"name": "viewport"}):
            score += 10
        else:
            issues.append("Not mobile optimized")

        # Trust signals
        links = [a.get("href", "") for a in soup.find_all("a")]
        if any("contact" in l.lower() for l in links):
            score += 10
        else:
            issues.append("No contact page found")

    except Exception as e:
        issues.append(str(e))

    return {
        "score": min(score, 100),
        "issues": issues
    }


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
def run():
    st.markdown("## 📈 Business Compare")
    st.markdown(
        "Compare your business website against competitors using **real performance & SEO signals**."
    )

    st.divider()

    your_site = st.text_input(
        "Your Website",
        placeholder="https://yourbusiness.com"
    )

    st.markdown("### Competitor Websites")
    comp1 = st.text_input("Competitor 1", placeholder="https://competitor1.com")
    comp2 = st.text_input("Competitor 2", placeholder="https://competitor2.com")
    comp3 = st.text_input("Competitor 3", placeholder="https://competitor3.com")

    competitors = [c for c in [comp1, comp2, comp3] if c]

    if st.button("Run Comparison"):
        if not your_site or not competitors:
            st.warning("Please enter your site and at least one competitor.")
            return

        with st.spinner("Analyzing websites..."):
            your_result = analyze_site(your_site)
            competitor_results = {
                url: analyze_site(url) for url in competitors
            }

        st.divider()
        st.subheader("📊 Comparison Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Score", your_result["score"])
        with col2:
            best_comp = max(competitor_results.items(), key=lambda x: x[1]["score"])
            st.metric("Best Competitor", best_comp[1]["score"])

        st.divider()
        st.markdown("### 🔍 Detailed Breakdown")

        st.markdown(f"#### 🟢 Your Website ({your_site})")
        st.write("Score:", your_result["score"])
        if your_result["issues"]:
            for i in your_result["issues"]:
                st.write("•", i)
        else:
            st.success("No major issues")

        for site, result in competitor_results.items():
            st.markdown(f"#### 🔵 Competitor ({site})")
            st.write("Score:", result["score"])
            if result["issues"]:
                for i in result["issues"]:
                    st.write("•", i)
            else:
                st.success("No major issues")

        st.caption(
            "Comparison based on real website SEO, performance, and accessibility signals."
        )
