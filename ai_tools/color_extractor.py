import streamlit as st
from PIL import Image
from collections import Counter
from services.insights_store import save_insight
from services.caption_engine import generate_caption

def extract_colors(image, num_colors=5):
    image = image.resize((150, 150))
    pixels = list(image.getdata())
    most_common = Counter(pixels).most_common(num_colors)
    return [color for color, _ in most_common]

def run():
    st.markdown("### 🎨 Brand Color Extractor")

    user_id = st.session_state.get("user_id", "guest")

    uploaded_file = st.file_uploader(
        "Upload brand logo or creative",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        colors = extract_colors(image)

        st.markdown("#### 🎯 Extracted Brand Colors")
        for color in colors:
            st.markdown(
                f"<div style='background-color: rgb{color}; padding:10px; border-radius:6px; color:white;'>RGB {color}</div>",
                unsafe_allow_html=True
            )

        insights = {
            "dominant_colors_rgb": colors,
            "palette_size": len(colors),
            "brand_mood": "bold" if colors[0][0] > 150 else "calm"
        }

        # 1️⃣ Save insight
        save_insight(
            user_id=user_id,
            tool="Color Extractor",
            data=insights
        )

        # 2️⃣ Generate AI caption
        caption_prompt = generate_caption(
            insight=insights,
            tone="creative",
            platform="Instagram"
        )

        st.success("Color insights saved to Dashboard ✅")

        st.markdown("#### ✨ AI Caption Suggestion")
        st.text_area("Caption", caption_prompt, height=200)

