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
if selected == "Dashboard":
    st.header("📊 Unified Analytics Dashboard")

    if "dashboard_data" not in st.session_state or not st.session_state["dashboard_data"]:
        st.info("Run any tool to populate the dashboard with real data.")
    else:
        for tool_name, df in st.session_state["dashboard_data"].items():
            st.subheader(f"📌 {tool_name}")
            
            # Show top 10 rows
            st.dataframe(df.head(10))

            # ---------------- Interactive Visualizations ----------------
            if tool_name.lower() in ["churn predictor", "churn"]:
                cols = ["Recency", "Frequency", "Monetary"]
                if all(col in df.columns for col in cols):
                    st.plotly_chart(px.bar(df[cols].fillna(0), title="Churn RFM Metrics"))

            if tool_name.lower() in ["clv calculator", "clv"]:
                if "CustomerID" in df.columns and "CLV" in df.columns:
                    st.plotly_chart(px.line(df, x="CustomerID", y="CLV", title="Customer Lifetime Value"))

            if tool_name.lower() in ["market trends", "market_trends"]:
                if "LastPurchaseDate" in df.columns and "TotalSpent" in df.columns:
                    trend = df.groupby(df["LastPurchaseDate"].dt.to_period("M"))["TotalSpent"].sum().reset_index()
                    trend["LastPurchaseDate"] = trend["LastPurchaseDate"].dt.to_timestamp()
                    st.plotly_chart(px.line(trend, x="LastPurchaseDate", y="TotalSpent", title="Monthly Total Spend Trend"))

            if tool_name.lower() in ["roi tracker", "roi_tracker"]:
                if "ad_name" in df.columns and "ROI" in df.columns:
                    st.plotly_chart(px.bar(df, x="ad_name", y="ROI", title="Campaign ROI (%)"))

            if tool_name.lower() in ["ad creative tester", "ad_creatives"]:
                if "ad_name" in df.columns and "CTR" in df.columns:
                    st.plotly_chart(px.bar(df, x="ad_name", y="CTR", title="Ad CTR Comparison"))

            # ---------------- AI Insight ----------------
            if "AI_Insight" in df.columns:
                st.success(f"💡 AI Insight: {df['AI_Insight'].iloc[0]}")

            st.markdown("---")

# ---------------- Dashboard Page ----------------
if selected == "Dashboard":
    st.header("📊 Unified Analytics Dashboard")

    if "dashboard_data" not in st.session_state or not st.session_state["dashboard_data"]:
        st.info("Run any tool to populate the dashboard with real data.")
    else:
        df_dict = st.session_state["dashboard_data"]

        # ---------------- Filters ----------------
        st.subheader("⚙️ Filters")
        filter_tool = st.selectbox("Select Tool to Filter", ["All"] + list(df_dict.keys()))
        date_filter = st.date_input("Select Start Date", value=None)

        # ---------------- KPI Cards ----------------
        st.subheader("📌 Summary KPIs")
        kpi_cols = st.columns(5)

        churn_df = df_dict.get("churn", df_dict.get("Churn Predictor", pd.DataFrame()))
        clv_df = df_dict.get("clv", df_dict.get("CLV Calculator", pd.DataFrame()))
        roi_df = df_dict.get("roi_tracker", df_dict.get("ROI Tracker", pd.DataFrame()))
        trends_df = df_dict.get("market_trends", df_dict.get("Market Trends", pd.DataFrame()))
        ads_df = df_dict.get("ad_creatives", df_dict.get("Ad Creative Tester", pd.DataFrame()))

        kpi_cols[0].metric("Total Customers", len(churn_df))
        kpi_cols[1].metric("Avg CLV", round(clv_df["CLV"].mean(),2) if not clv_df.empty else 0)
        kpi_cols[2].metric("Predicted Churn %", round(churn_df["ChurnPrediction"].mean()*100,2) if "ChurnPrediction" in churn_df else 0)
        kpi_cols[3].metric("Total ROI %", round(roi_df["ROI"].sum(),2) if "ROI" in roi_df else 0)
        kpi_cols[4].metric("Top CTR %", round(ads_df["CTR"].max(),2) if "CTR" in ads_df else 0)

        st.markdown("---")

        # ---------------- Show Visualizations ----------------
        for tool_name, df in df_dict.items():
            if filter_tool != "All" and filter_tool != tool_name:
                continue

            st.subheader(f"📌 {tool_name}")
            
            # Apply date filter if applicable
            if date_filter and "LastPurchaseDate" in df.columns:
                df = df[df["LastPurchaseDate"] >= pd.to_datetime(date_filter)]

            st.dataframe(df.head(10))

            # ---------------- Interactive Charts ----------------
            if tool_name.lower() in ["churn predictor", "churn"]:
                cols = ["Recency", "Frequency", "Monetary"]
                if all(col in df.columns for col in cols):
                    st.plotly_chart(px.bar(df[cols].fillna(0), title="Churn RFM Metrics"))

            if tool_name.lower() in ["clv calculator", "clv"]:
                if "CustomerID" in df.columns and "CLV" in df.columns:
                    st.plotly_chart(px.line(df, x="CustomerID", y="CLV", title="Customer Lifetime Value"))

            if tool_name.lower() in ["market trends", "market_trends"]:
                if "LastPurchaseDate" in df.columns and "TotalSpent" in df.columns:
                    trend = df.groupby(df["LastPurchaseDate"].dt.to_period("M"))["TotalSpent"].sum().reset_index()
                    trend["LastPurchaseDate"] = trend["LastPurchaseDate"].dt.to_timestamp()
                    st.plotly_chart(px.line(trend, x="LastPurchaseDate", y="TotalSpent", title="Monthly Total Spend Trend"))

            if tool_name.lower() in ["roi tracker", "roi_tracker"]:
                if "ad_name" in df.columns and "ROI" in df.columns:
                    st.plotly_chart(px.bar(df, x="ad_name", y="ROI", title="Campaign ROI (%)"))

            if tool_name.lower() in ["ad creative tester", "ad_creatives"]:
                if "ad_name" in df.columns and "CTR" in df.columns:
                    st.plotly_chart(px.bar(df, x="ad_name", y="CTR", title="Ad CTR Comparison"))

            # ---------------- AI Insight ----------------
            if "AI_Insight" in df.columns:
                st.success(f"💡 AI Insight: {df['AI_Insight'].iloc[0]}")

            # ---------------- Export Button ----------------
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"📥 Download {tool_name} CSV",
                data=csv,
                file_name=f"{tool_name.replace(' ','_').lower()}.csv",
                mime="text/csv"
            )

            st.markdown("---")

