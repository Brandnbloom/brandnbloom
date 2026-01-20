# ai_tools/color_extractor.py

import streamlit as st
from PIL import Image
import numpy as np
from collections import Counter


def extract_colors(image: Image.Image, k: int = 5):
    img = image.resize((150, 150))
    img = np.array(img)

    pixels = img.reshape(-1, 3)
    pixels = [tuple(p) for p in pixels]

    common = Counter(pixels).most_common(k)
    return [color for color, _ in common]


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def run():
    st.markdown("## 🎨 Color Extractor")
    st.markdown("Upload your brand image to extract dominant colors.")

    uploaded = st.file_uploader(
        "Upload logo / banner / creative",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded Image", width=300)

        colors = extract_colors(image)

        st.markdown("### 🎯 Dominant Colors")

        cols = st.columns(len(colors))
        luminances = []

        for i, rgb in enumerate(colors):
            hex_code = rgb_to_hex(rgb)
            lum = luminance(rgb)
            luminances.append(lum)

            with cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        background:{hex_code};
                        height:80px;
                        border-radius:10px;
                        border:1px solid #ccc;">
                    </div>
                    <p style="text-align:center">{hex_code}</p>
                    """,
                    unsafe_allow_html=True
                )

        avg_lum = sum(luminances) / len(luminances)

        st.markdown("### 🧠 Brand Insight")

        if avg_lum < 120:
            st.success("This is a **Dark / Premium** palette.")
            st.write("Best for luxury, tech, premium brands.")
        else:
            st.success("This is a **Light / Friendly** palette.")
            st.write("Great for wellness, lifestyle, and consumer brands.")

        st.markdown("### 💡 Suggestions")
        st.write("• Keep 1 primary + 2 accent colors")
        st.write("• Ensure text contrast for accessibility")
        st.write("• Stay consistent across socials & website")
