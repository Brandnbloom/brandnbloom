import streamlit as st
import re


PLATFORM_LIMITS = {
    "Instagram": 30,
    "LinkedIn": 5,
    "Twitter / X": 3
}


INTENT_HASHTAGS = {
    "Branding": [
        "branding", "brandidentity", "brandstrategy",
        "brandbuilding", "personalbrand"
    ],
    "Education": [
        "learning", "education", "knowledge",
        "growthmindset", "skillbuilding"
    ],
    "Marketing": [
        "marketing", "digitalmarketing", "contentmarketing",
        "businessgrowth", "onlinemarketing"
    ],
    "Sales": [
        "sales", "leadgeneration", "funnels",
        "conversion", "growthhacking"
    ],
}


def sanitize_keyword(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return text.replace(" ", "")


def generate_hashtags(
    keyword: str,
    platform: str,
    intent: str,
    niche: str
):
    base = sanitize_keyword(keyword)
    niche_clean = sanitize_keyword(niche)

    hashtags = []

    # Keyword-based
    hashtags.extend([
        f"#{base}",
        f"#{base}tips",
        f"#{base}strategy",
        f"#{base}growth",
    ])

    # Niche-based
    if niche_clean:
        hashtags.extend([
            f"#{niche_clean}",
            f"#{niche_clean}business",
            f"#{niche_clean}community",
        ])

    # Intent-based
    for tag in INTENT_HASHTAGS.get(intent, []):
        hashtags.append(f"#{tag}")

    # Platform-specific behavior
    if platform == "Instagram":
        hashtags.extend([
            "#instagrowth", "#reels", "#contentcreator",
            "#explorepage", "#socialmedia"
        ])

    elif platform == "LinkedIn":
        hashtags.extend([
            "#linkedin", "#b2b", "#founders",
            "#professionallife", "#careerdevelopment"
        ])

    else:  # Twitter / X
        hashtags.extend([
            "#startups", "#marketingtips", "#buildinpublic"
        ])

    # Remove duplicates while preserving order
    seen = set()
    final = []
    for h in hashtags:
        if h not in seen:
            final.append(h)
            seen.add(h)

    return final[:PLATFORM_LIMITS.get(platform, 10)]


def run():
    st.markdown("## 🔖 Hashtag Recommender")
    st.markdown(
        "Generate **relevant, intent-driven hashtags** optimized for each platform."
    )

    st.divider()

    # =========================
    # INPUTS (REAL)
    # =========================
    keyword = st.text_input(
        "Primary Keyword",
        placeholder="e.g. brand strategy, content marketing"
    )

    niche = st.text_input(
        "Niche / Industry (optional)",
        placeholder="e.g. fashion, SaaS, food, fitness"
    )

    platform = st.selectbox(
        "Platform",
        ["Instagram", "LinkedIn", "Twitter / X"]
    )

    intent = st.selectbox(
        "Content Intent",
        ["Branding", "Education", "Marketing", "Sales"]
    )

    st.divider()

    # =========================
    # OUTPUT
    # =========================
    if st.button("Generate Hashtags"):
        if not keyword:
            st.warning("Please enter a primary keyword.")
            return

        hashtags = generate_hashtags(
            keyword=keyword,
            platform=platform,
            intent=intent,
            niche=niche
        )

        st.markdown("### ✅ Recommended Hashtags")
        st.code(" ".join(hashtags))

        st.caption(
            f"Limit respected: {PLATFORM_LIMITS[platform]} hashtags for {platform}"
        )

        st.info(
            "🔗 Next upgrade: connect Instagram / LinkedIn trend APIs "
            "for real-time hashtag popularity & competition scores."
        )
