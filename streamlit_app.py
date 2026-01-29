import streamlit as st

# Utils
from utils.session import get_user_id
from utils.usage_limiter import check_usage, show_limit_message
from utils.dashboard import load_dashboard_data
from utils.pdf_export import generate_pdf_report

# Services
from services.razorpay_service import get_razorpay_customers

# Tools
from ai_tools.customer_360_rfm import run_customer_360_rfm_tool
from ai_tools.ad_creative_tester import run_ad_creative_tester
from ai_tools.churn_predictor import run_churn_predictor
from ai_tools.clv_calculator import run_clv_calculator
from ai_tools.market_trends import run_market_trends
from ai_tools.roi_tracker import run_roi_tracker
from ai_tools.rfm_segmentation import run_rfm_analysis
from ai_tools.sentiment_analyzer import run_sentiment_analyzer
from ai_tools.audit_tools import run_audit_tools

st.set_page_config(page_title="Brand N Bloom", layout="wide")

user_id = get_user_id()

# ---------------- MENU ----------------

menu = [
    "Home",
    "Customer 360 + RFM",
    "CLV + Churn ML",
    "Market Trends",
    "ROI Tracker",
    "Audit Tools",
    "Dashboard / PDF Export"
]

selected = st.selectbox("Select Tool", menu)

# ---------------- HOME ----------------

if selected == "Home":
    st.title("🌸 Brand N Bloom")

    st.success("AI Powered Marketing & Customer Analytics")

    st.markdown("""
    • Customer 360  
    • RFM Segmentation  
    • CLV Prediction  
    • Churn ML  
    • ROI Tracking  
    • Automated Reports  
    """)

# ---------------- CUSTOMER 360 ----------------

elif selected == "Customer 360 + RFM":

    if check_usage("customer_360"):

        df_ga = load_dashboard_data(user_id)      # temp placeholder
        df_meta = load_dashboard_data(user_id)    # temp placeholder
        df_razorpay = get_razorpay_customers()

        run_customer_360_rfm_tool(df_ga, df_razorpay, df_meta)

    else:
        show_limit_message(user_id)

# ---------------- CLV + CHURN ----------------

elif selected == "CLV + Churn ML":

    if check_usage("clv_churn"):
        run_clv_calculator(user_id)
        run_churn_predictor(user_id)
    else:
        show_limit_message(user_id)

# ---------------- MARKET ----------------

elif selected == "Market Trends":

    if check_usage("market"):
        run_market_trends(user_id)
    else:
        show_limit_message(user_id)

# ---------------- ROI ----------------

elif selected == "ROI Tracker":

    if check_usage("roi"):
        run_roi_tracker(user_id)
    else:
        show_limit_message(user_id)

# ---------------- AUDIT ----------------

elif selected == "Audit Tools":

    if check_usage("audit"):
        run_audit_tools(user_id)
    else:
        show_limit_message(user_id)

# ---------------- DASHBOARD ----------------

elif selected == "Dashboard / PDF Export":

    st.title("Dashboard")

    data = load_dashboard_data(user_id)
    st.dataframe(data)

    if st.button("Download PDF"):

        path = generate_pdf_report(user_id, data)

        with open(path, "rb") as f:
            st.download_button(
                "Download Report",
                f,
                file_name="brandnbloom.pdf"
            )
