import streamlit as st
import pandas as pd
import plotly.express as px

# Utils
from utils.session import get_user_id
from utils.usage_limiter import check_usage, show_limit_message
from utils.dashboard import load_dashboard_data
from utils.pdf_export import generate_pdf_report
from utils.visualization import show_numeric_bar_chart

# Services
from services.razorpay_service import get_razorpay_customers
from services.pdf_export import export_dashboard_pdf
from services.user_api import init_db, add_user, authenticate_user, get_usage, update_usage
import json

# Tools
from ai_tools.customer_360_rfm import run_customer_360_rfm_tool
from ai_tools.churn_predictor import run_churn_predictor
from ai_tools.clv_calculator import run_clv_calculator
from ai_tools.market_trends import run_market_trends
from ai_tools.marketing_roi import run_marketing_roi
from ai_tools.audit_tools import run_audit_tools

st.set_page_config(page_title="Brand N Bloom", layout="wide")

user_id = get_user_id()

def check_usage(tool_name, free_limit=3):
    """
    Checks if the user has free usage left for a tool.
    Increments usage count if allowed.
    """
    usage = st.session_state["tool_usage"].get(tool_name, 0)
    if usage < free_limit:
        st.session_state["tool_usage"][tool_name] = usage + 1
        remaining = free_limit - st.session_state["tool_usage"][tool_name]
        st.info(f"✅ Free usage remaining for '{tool_name}': {remaining}")
        return True
    else:
        st.warning(f"❌ Free limit reached for '{tool_name}'. Please subscribe to continue.")
        return False

init_db()
if selected == "Login":
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.success("Login successful!")
            st.session_state["user_email"] = email
            # Load persistent usage
            st.session_state["tool_usage"] = get_usage(email)
        else:
            st.error("Invalid credentials")

elif selected == "Signup":
    st.subheader("🆕 Signup")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        if add_user(email, password):
            st.success("Account created! Please login.")
        else:
            st.error("Email already exists")


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

# ---------------- CUSTOMER 360 ----------------

elif selected == "Customer 360 + RFM":

    if check_usage("customer_360"):

        df_ga = pd.DataFrame()      # later GA4
        df_meta = pd.DataFrame()    # later Meta
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

elif selected == "Marketing ROI":

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

    st.title("📊 Dashboard")

    data = load_dashboard_data(user_id)

    if not data:
        st.info("Run tools to populate dashboard.")
        st.stop()

    for tool, df in data.items():

        st.subheader(tool)
        st.dataframe(df.head())

        show_numeric_bar_chart(df, tool)

if st.button("📄 Export Full PDF Report"):
    if "dashboard_data" not in st.session_state or not st.session_state["dashboard_data"]:
        st.warning("No data available. Run some tools first!")
    else:
        pdf_buffer = export_dashboard_pdf(st.session_state["dashboard_data"])
        st.download_button(
            label="📥 Download Full PDF Report",
            data=pdf_buffer,
            file_name="BrandNBloom_Full_Report.pdf",
            mime="application/pdf"
        )

def check_usage(tool_name, free_limit=3):
    """
    Checks if the user has free usage left for a tool.
    If exceeded, prompts subscription.
    """
    usage = st.session_state["tool_usage"].get(tool_name, 0)

    # If user has paid subscription, ignore limits
    if st.session_state.get("user_subscribed", False):
        return True

    if usage < free_limit:
        st.session_state["tool_usage"][tool_name] = usage + 1
        st.info(f"✅ Free usage remaining for '{tool_name}': {free_limit - st.session_state['tool_usage'][tool_name]}")

        # Persist usage if logged in
        if "user_email" in st.session_state:
            from services.user_api import update_usage
            update_usage(st.session_state["user_email"], st.session_state["tool_usage"])
        return True
    else:
        st.warning(f"❌ Free limit reached for '{tool_name}'.")

        # Show subscription prompt
        st.markdown("""
        <div style='border:1px solid #F1C0D1; padding:10px; border-radius:10px; background-color:#FFF0F5'>
        💳 **Upgrade to Pro to unlock unlimited access!**  
        - Unlimited tool usage  
        - Unlimited PDF exports  
        - Priority AI insights  

        <a href='https://yourpaymentlink.com' target='_blank'>
        <button style='padding:10px 20px; background-color:#FF69B4; color:white; border:none; border-radius:5px;'>Subscribe Now</button>
        </a>
        </div>
        """, unsafe_allow_html=True)
        return False

