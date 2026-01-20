# ai_tools/hashtag_recommender.py

import streamlit as st


BASE_HASHTAGS = {
    "Brand": [
        "#branding", "#brandidentity", "#brandstrategy",
        "#brandbuilding", "#personalbrand"
    ],
    "Educational": [
        "#learn", "#education", "#knowledge",
        "#growthmindset", "#learningdaily"
    ],
    "Promotional": [
        "#marketing", "#digitalmarketing", "#businessgrowth",
        "#onlinemarketing", "#sales"
    ],
}

PLATFORM_HASHTAGS = {
    "Instagram": [
        "#instagrowth", "#instagrammarketing",
        "#reels", "#instadaily", "#contentcreator"
    ],
    "LinkedIn": [
        "#linkedinmarketing", "#b2b", "#founders",
        "#professionallife", "#careergrowth"
    ],
}


def generate_hashtags(topic, platform, content_type):
    topic_tags = [
        f"#{topic.replace(' ', '')}",
        f"#{topic.replace(' ', '')}tips",
        f"#{topic.replace(' ', '')}business",
    ]

    hashtags = (
        topic_tags
        + BASE_HASHTAGS.get(content_type, [])
        + PLATFORM_HASHTAGS.get(platform, [])
    )

    # remove duplicates while preserving order
    seen = set()
    final_tags = []
    for tag in hashtags:
        if tag not in seen:
            final_tags.append(tag)
            seen.add(tag)

    return final_tags[:20]


def run():
    st.markdown("## 🔖 Hashtag Recommender")
    st.markdown("Generate relevant, high-performing hashtags in seconds.")

    topic = st.text_input("Main topic or keyword")
    platform = st.selectbox("Platform", ["Instagram", "LinkedIn"])
    content_type = st.selectbox(
        "Content type",
        ["Brand", "Educational", "Promotional"]
    )

    if st.button("Generate Hashtags"):
        if not topic:
            st.warning("Please enter a topic.")
            return

        hashtags = generate_hashtags(topic, platform, content_type)

        st.markdown("### ✅ Recommended Hashtags")
        st.code(" ".join(hashtags))
