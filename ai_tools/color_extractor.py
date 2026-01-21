# ai_tools/color_extractor.py

import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def extract_colors(image, num_colors=5):
    img = image.resize((200, 200))
    img_array = np.array(img)
    img_array = img_array.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(img_array)

    colors = kmeans.cluster_centers_.astype(int)
    return colors


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def run():
    st.markdown("## 🎨 Color Extractor")
    st.markdown("Upload your brand logo or image to extract dominant colors.")

    uploaded_file = st.file_uploader(
        "Upload an image (PNG, JPG)",
        type=["png", "jpg", "jpeg"]
    )

    num_colors = st.slider("Number of colors", 3, 8, 5)

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("Extracting colors..."):
            colors = extract_colors(image, num_colors)

        st.markdown("### 🎯 Extracted Brand Colors")

        cols = st.columns(len(colors))
        for i, color in enumerate(colors):
            hex_code = rgb_to_hex(color)
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        background-color:{hex_code};
                        height:120px;
                        border-radius:10px;
                        margin-bottom:8px;
                    "></div>
                    <p style="text-align:center;"><strong>{hex_code}</strong></p>
                    """,
                    unsafe_allow_html=True
                )

        st.success("✅ Color palette extracted successfully")
