import streamlit as st


# -------------------------------------------------
# CAPTION LOGIC ENGINE
# -------------------------------------------------
def generate_caption(insight, audience, goal, platform, tone):
    hooks = {
        "Instagram": [
            "Nobody tells you this 👀",
            "This changed everything for us 🔥",
            "If you're struggling with this, read this 👇",
        ],
        "LinkedIn": [
            "Here’s a lesson most professionals learn too late:",
            "One hard truth about growth:",
            "This insight changed how I work:",
        ],
    }

    cta = {
        "Awareness": "What do you think?",
        "Engagement": "Comment your thoughts 👇",
        "Conversion": "DM us to get started.",
    }

    tone_modifier = {
        "Professional": "",
        "Friendly": "😊",
        "Bold": "🔥",
        "Inspirational": "✨",
    }

    hook = hooks[platform][0]
    ending = cta[goal]

    caption = f"""{hook}

{insight}

This matters especially for {audience.lower()}.

{ending} {tone_modifier[tone]}
"""

    return caption.strip()


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
def run():
    st.markdown("## 🧠 Insights → Caption")
    st.markdown(
        "Turn **insights & data** into high-impact captions that actually convert."
    )

    st.divider()

    insight = st.text_area(
        "Core insight / data point",
        placeholder="Example: Brands that post consistently grow 3x faster."
    )

    audience = st.text_input(
        "Target audience",
        placeholder="Founders, small business owners, creators"
    )

    platform = st.selectbox(
        "Platform",
        ["Instagram", "LinkedIn"]
    )

    goal = st.selectbox(
        "Primary goal",
        ["Awareness", "Engagement", "Conversion"]
    )

    tone = st.selectbox(
        "Tone",
        ["Professional", "Friendly", "Bold", "Inspirational"]
    )

    if st.button("Generate Caption"):
        if not insight or not audience:
            st.warning("Please fill all required fields.")
            return

        caption = generate_caption(
            insight=insight,
            audience=audience,
            goal=goal,
            platform=platform,
            tone=tone
        )

        st.divider()
        st.markdown("### ✨ Generated Caption")
        st.code(caption)
