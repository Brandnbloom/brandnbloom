# ai_tools/insights_caption.py

import streamlit as st
import random


CAPTION_TEMPLATES = {
    "Instagram": [
        "✨ {hook}\n\n{body}\n\n{cta} {hashtags}",
        "{hook}\n\n{body}\n\n👇 {cta}\n{hashtags}",
    ],
    "LinkedIn": [
        "{hook}\n\n{body}\n\n👉 {cta}",
        "{hook}\n\n{body}\n\nThoughts?",
    ],
    "Twitter": [
        "{hook}\n\n{body}\n\n{cta}",
    ]
}


HASHTAGS = [
    "#branding", "#marketing", "#startup", "#business",
    "#creatoreconomy", "#growth", "#brandstrategy"
]


def generate_hook(topic, tone):
    hooks = {
        "Professional": [
            f"Here’s what most brands miss about {topic}.",
            f"A simple insight that can change how you view {topic}.",
        ],
        "Friendly": [
            f"Let’s talk about {topic} 💬",
            f"Quick thoughts on {topic} 👇",
        ],
        "Bold": [
            f"Stop ignoring this about {topic}.",
            f"{topic} isn’t the problem. Your strategy is.",
        ],
        "Emotional": [
            f"If you’re struggling with {topic}, read this.",
            f"This changed how I feel about {topic}.",
        ],
    }
    return random.choice(hooks[tone])


def generate_body(topic, tone):
    return (
        f"{topic} plays a huge role in how your audience perceives your brand. "
        "Consistency, clarity, and intent matter more than trends. "
        "Focus on connection before conversion."
    )


def generate_cta(platform):
    ctas = {
        "Instagram": "Save this for later",
        "LinkedIn": "Let’s discuss in comments",
        "Twitter": "Retweet if you agree",
    }
    return ctas[platform]


def run():
    st.markdown("## ✍️ Insights to Caption")
    st.markdown("Turn ideas into high-impact captions instantly.")

    topic = st.text_input("What is your post about?")
    tone = st.selectbox(
        "Select tone",
        ["Professional", "Friendly", "Bold", "Emotional"]
    )
    platform = st.selectbox(
        "Platform",
        ["Instagram", "LinkedIn", "Twitter"]
    )

    if st.button("Generate Captions"):
        if not topic:
            st.warning("Please enter a topic.")
            return

        st.markdown("### 📌 Generated Captions")

        for i in range(3):
            hook = generate_hook(topic, tone)
            body = generate_body(topic, tone)
            cta = generate_cta(platform)
            hashtags = " ".join(random.sample(HASHTAGS, 4))

            template = random.choice(CAPTION_TEMPLATES[platform])
            caption = template.format(
                hook=hook,
                body=body,
                cta=cta,
                hashtags=hashtags,
            )

            st.text_area(
                f"Caption {i+1}",
                caption,
                height=180
            )
