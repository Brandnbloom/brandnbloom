import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote


# -------------------------------------------------
# SEARCH ENGINE
# -------------------------------------------------
def google_search(query, num_results=5):
    url = f"https://www.google.com/search?q={quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for g in soup.select("div.tF2Cxc")[:num_results]:
        title = g.select_one("h3")
        link = g.select_one("a")
        snippet = g.select_one("div.VwiC3b")

        if title and link:
            results.append({
                "name": title.text,
                "url": link["href"],
                "bio": snippet.text if snippet else ""
            })

    return results


# -------------------------------------------------
# INFLUENCER SCORING
# -------------------------------------------------
def score_influencer(bio, keyword):
    score = 0
    bio_lower = bio.lower()

    if keyword.lower() in bio_lower:
        score += 40

    engagement_words = [
        "founder", "coach", "creator", "community",
        "educator", "speaker", "expert"
    ]

    for w in engagement_words:
        if w in bio_lower:
            score += 10

    return min(score, 100)


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
def run():
    st.markdown("## 🤝 Influencer Finder")
    st.markdown(
        "Discover **real creators & thought leaders** aligned with your brand."
    )

    st.divider()

    keyword = st.text_input("Brand niche / keyword", placeholder="fitness, skincare, startups")
    platform = st.selectbox("Platform", ["Instagram", "LinkedIn"])

    if st.button("Find Influencers"):
        if not keyword:
            st.warning("Please enter a keyword.")
            return

        query = f"site:{'instagram.com' if platform == 'Instagram' else 'linkedin.com'} {keyword}"

        with st.spinner("Searching influencers..."):
            try:
                results = google_search(query)
            except Exception as e:
                st.error(f"Search failed: {e}")
                return

        if not results:
            st.info("No influencers found. Try a different keyword.")
            return

        st.divider()
        st.markdown("### 🎯 Influencers Found")

        for r in results:
            score = score_influencer(r["bio"], keyword)

            st.markdown(
                f"""
                **{r['name']}**  
                🔗 {r['url']}  
                🧠 Relevance Score: **{score}/100**  
                📝 {r['bio']}
                """
            )
            st.divider()
