import streamlit as st
from PIL import Image
import pytesseract
from textblob import TextBlob
import pandas as pd

sample_data = pd.DataFrame({
    "customer_id": [1,2,3],
    "recency": [10, 20, 5],
    "frequency": [3, 1, 5],
    "monetary": [200, 150, 500],
    "churn": [0, 1, 0]
})

st.download_button(
    "📥 Download Sample Data",
    data=sample_data.to_csv(index=False),
    file_name="sample_data.csv",
    mime="text/csv"
)

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

  # ---------------- Check usage ----------------
    from streamlit_app import check_usage
    if not check_usage("OCR Sentiment"):
        st.stop()  # Stop the tool if free limit reached

    # ---------------- Tool logic ----------------
    uploaded_file = st.file_uploader("Upload Customer Data", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")
        # Your OCR Sentiment logic here...

