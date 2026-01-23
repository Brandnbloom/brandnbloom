import streamlit as st
from services.storage import load_insights
from services.insights_store import get_insights

def run():
    st.markdown("## 📊 Brand Intelligence Dashboard")

data = load_insights()

if not data:
    st.warning("No insights generated yet.")
    return

st.subheader("Saved Brand Insights")

for tool, insights in data.items():
    st.markdown(f"### {tool}")
    st.json(insights)
user_id = st.session_state.get("user_id", "guest")

insights = get_insights(user_id)

if not insights:
    st.info("No insights yet. Run a tool to see results.")
else:
    for item in insights:
        st.markdown(f"### 🔍 {item['tool']}")
        st.json(item["data"])
        st.caption(item["timestamp"])
