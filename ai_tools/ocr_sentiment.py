import streamlit as st
from PIL import Image
import pytesseract
from textblob import TextBlob

def run():
    st.markdown("## 🖼️ OCR Sentiment Analyzer")
    st.markdown(
        "Upload an image, extract the text, and analyze its sentiment."
    )

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # OCR
        try:
            text = pytesseract.image_to_string(image)
            if not text.strip():
                st.warning("No text detected in the image.")
                return
            st.markdown("### Extracted Text")
            st.code(text)

            # Sentiment Analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity

            if polarity > 0.1:
                sentiment = "Positive 😊"
            elif polarity < -0.1:
                sentiment = "Negative 😞"
            else:
                sentiment = "Neutral 😐"

            st.markdown(f"### Sentiment: **{sentiment}**")
        except Exception as e:
            st.error(f"OCR failed: {e}")
