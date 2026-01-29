from services.customer_api import get_customer_data
from services.instagram_api import get_posts

def run():
    df_customers = get_customer_data()
    social_df = get_posts("brand")

    # RFM + Sentiment logic here

  # ---------------- Check usage ----------------
    from streamlit_app import check_usage
    if not check_usage("Segmentation sentiment"):
        st.stop()  # Stop the tool if free limit reached

    # ---------------- Tool logic ----------------
    uploaded_file = st.file_uploader("Upload Customer Data", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")
        # Your Segmentation sentiment logic here...
