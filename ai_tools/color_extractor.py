# ai_tools/color_extractor.py

import streamlit as st
from PIL import Image
import numpy as np


def extract_colors(image, k=5):
    """
    Simple dominant color extraction using numpy clustering.
    """
    img = image.resize((200, 200))
    data = np.array(img).reshape(-1, 3)

    # random sampling for speed
    pixels = data[np.random.choice(data.shape[0], 1000, replace=False)]

    # k-means style clustering (manual, lightweight)
    colors = pixels[np.random.choice(len(pixels), k, replace=False)]

    for _ in range(8):
        distances = np.sqrt(((pixels[:, None] - colors[None, :]) ** 2).sum(axis=2))
        clusters = np.argmin(distances, axis=1)
        for i in range(k):
            if np.any(clusters == i):
                colors[i] = pixels[clusters == i].mean(axis=0)

    return colors.astype(int)


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def run():
    st.markdown("## 🎨 Color Extractor")
    st.markdown("Extract brand colors from logos, creatives, or banners.")

    file = st.file_uploader(
        "Upload an image (PNG / JPG)",
        type=["png", "jpg", "jpeg"]
    )

    if not file:
        st.info("Upload an image to extract colors.")
        return

    image = Image.open(file).convert("RGB")
    st.image(image, caption="Uploaded image", width=300)

    colors = extract_colors(image)

    st.markdown("### 🎯 Extracted Brand Colors")

    cols = st.columns(len(colors))
    for i, rgb in enumerate(colors):
        hex_color = rgb_to_hex(tuple(rgb))
        lum = luminance(rgb)

        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background:{hex_color};
                    height:80px;
                    border-radius:12px;
                    border:1px solid #ccc;
                "></div>
                <p style="text-align:center;margin-top:6px;">
                    <strong>{hex_color}</strong><br/>
                    {'Dark' if lum < 140 else 'Light'}
                </p>
                """,
                unsafe_allow_html=True,
            )
