import streamlit as st
import os

# ----------------------------
# Utils
# ----------------------------
from utils.session import get_user_id
from utils.usage_limiter import check_usage, show_limit_message
from utils.dashboard import load_dashboard_data
from utils.pdf_export import generate_pdf_report

# ----------------------------
# Tools (ai_tools)
# ----------------------------
from ai_tools.customer_360_rfm import run_customer_360_rfm_tool
from ai_tools.ad_creative_tester import run_ad_creative_tester
from ai_tools.churn_predictor import run_churn_predictor
from ai_tools.clv_calculator import run_clv_calculator
from ai_tools.market_trends import run_market_trends
from ai_tools.roi_tracker import run_roi_tracker
from ai_tools.rfm_segmentation import run_rfm_analysis
from ai_tools.sentiment_analyzer import run_sentiment_analyzer
from ai_tools.audit_tools import run_audit_tools
st.set_page_config(page_title="Brand N Bloom Analytics", layout="wide")

st.title("🌸 Brand N Bloom Analytics Suite")

# ---------------- Top Menu ----------------
menu_options = ["Home", "Churn Predictor", "CLV Calculator", "Dashboard"]
selected = st.radio("Navigate", menu_options, horizontal=True)

# ---------------- Pages ----------------
if selected == "Home":
    st.markdown("## Welcome to Brand N Bloom Analytics Suite")
    st.markdown("Use the menu above to navigate between tools.")
elif selected == "Churn Predictor":
    run_churn()

elif selected == "CLV Calculator":
    run_clv()

elif selected == "Dashboard":
    st.header("📊 Central Dashboard")
    
    if "dashboard_data" not in st.session_state or not st.session_state["dashboard_data"]:
        st.info("No data yet. Run Churn Predictor or CLV Calculator to populate dashboard.")
    else:
        for tool_name, df in st.session_state["dashboard_data"].items():
            st.subheader(f"Results: {tool_name}")
            st.dataframe(df.head(10))
            
            # Interactive charts
            if "Recency" in df.columns and "Frequency" in df.columns and "Monetary" in df.columns:
                st.bar_chart(df[["Recency", "Frequency", "Monetary"]].fillna(0))
            
            if "CLV" in df.columns:
                st.line_chart(df[["CustomerID", "CLV"]].set_index("CustomerID"))

            # AI Insight
            if "AI_Insight" in df.columns:
                st.success(f"💡 AI Insight: {df['AI_Insight'].iloc[0]}")


# ----------------------------
# User Session
# ----------------------------
user_id = get_user_id()  # from utils/session.py

# ----------------------------
# Top Menu Bar
# ----------------------------
menu = [
    "Home",
    "Customer 360 + RFM",
    "Ad Creative Tester",
    "CLV + Churn ML",
    "Market Trends",
    "ROI Tracker",
    "Segmentation + Sentiment",
    "Audit Tools",
    "Dashboard / PDF Export"
]

selected = st.selectbox("🔹 Select Tool", menu)

# ----------------------------
# Tool Execution
# ----------------------------

# 0️⃣ Enhanced Home
if selected == "Home":
    # Custom CSS for banner & cards
    st.markdown(
        """
        <style>
        .home-banner {
            background: linear-gradient(120deg, #A7E7F0, #539788, #F2DCE3);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            color: #1D2233;
            font-family: 'Inter', sans-serif;
        }
        .kpi-card {
            background-color: #ffffffdd;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 2px 2px 10px #aaa;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Banner
    st.markdown("""
    <div class="home-banner">
        <h1>Welcome to Brand N Bloom 🌱</h1>
        <h3>Your AI-powered Marketing & Analytics Suite</h3>
        <p>Track, analyze, and optimize your campaigns all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # KPI Cards
    dashboard_data = load_dashboard_data(user_id)
    total_tools = 8
    free_uses = 3
    used_uses = sum([d.get("usage_count", 0) for d in dashboard_data])
    reports_generated = len([d for d in dashboard_data if d.get("chart_paths")])

    cols = st.columns(4)

    with cols[0]:
        st.markdown(f'<div class="kpi-card"><h2>{free_uses - used_uses}</h2><p>Free Uses Left</p></div>', unsafe_allow_html=True)

    with cols[1]:
        st.markdown(f'<div class="kpi-card"><h2>{total_tools}</h2><p>Total Tools</p></div>', unsafe_allow_html=True)

    with cols[2]:
        st.markdown(f'<div class="kpi-card"><h2>{len(dashboard_data)}</h2><p>Active Users</p></div>', unsafe_allow_html=True)

    with cols[3]:
        st.markdown(f'<div class="kpi-card"><h2>{reports_generated}</h2><p>Reports Generated</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Call-to-action
    if used_uses >= free_uses:
        st.warning("🚀 You have reached your free usage limit!")
        st.markdown("[Upgrade Now](#)", unsafe_allow_html=True)
    else:
        st.info("🌟 You still have free tool uses left! Explore and optimize your campaigns.")


# 1️⃣ Customer 360 + RFM
elif selected == "Customer 360 + RFM":
    if check_usage("customer_360"):
        df_ga = ...  # call GA service
        df_razorpay = ...  # call Razorpay service
        df_meta = ...  # call Meta Pixel service
        run_customer_360_rfm_tool(df_ga, df_stripe, df_meta)
    else:
        show_limit_message(user_id)

# 2️⃣ Ad Creative Tester
elif selected == "Ad Creative Tester":
    if check_usage("ad_creative_tester"):
        run_ad_creative_tester(user_id)
    else:
        show_limit_message(user_id)

# 3️⃣ CLV + Churn ML
elif selected == "CLV + Churn ML":
    if check_usage("clv_churn"):
        run_clv_calculator(user_id)
        run_churn_predictor(user_id)
    else:
        show_limit_message(user_id)

# 4️⃣ Market Trends
elif selected == "Market Trends":
    if check_usage("market_trends"):
        run_market_trends(user_id)
    else:
        show_limit_message(user_id)

# 5️⃣ ROI Tracker
elif selected == "ROI Tracker":
    if check_usage("roi_tracker"):
        run_roi_tracker(user_id)
    else:
        show_limit_message(user_id)

# 6️⃣ Segmentation + Sentiment
elif selected == "Segmentation + Sentiment":
    if check_usage("segmentation_sentiment"):
        df_customers = ...  # real customer data
        df_social = ...  # real social posts
        run_rfm_analysis(df_customers)
        run_sentiment_analyzer(df_social)
    else:
        show_limit_message(user_id)

# 7️⃣ Audit Tools
elif selected == "Audit Tools":
    if check_usage("audit_tools"):
        run_audit_tools(user_id)
    else:
        show_limit_message(user_id)

# 8️⃣ Dashboard / PDF Export
elif selected == "Dashboard / PDF Export":
    st.title("📊 Dashboard & PDF Export")
    data = load_dashboard_data(user_id)
    st.dataframe(data)

    if st.button("📄 Download Full PDF Report"):
        pdf_path = generate_pdf_report(user_id, data)
        st.success("Report generated!")

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name="Brand_N_Bloom_Report.pdf",
                mime="application/pdf"
            )

