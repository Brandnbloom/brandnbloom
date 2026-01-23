import streamlit as st
from services.storage import load_insights
from services.insights_store import get_insights
from services.insights_store import save_insight
from services.caption_engine import generate_caption



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
result = {
    "engagement_rate": 4.2,
    "posting_consistency": "low"
}

save_insight(
    user_id="guest",
    tool="Audit Tools",
    data=result
)

caption_prompt = generate_caption(result)
st.text_area("AI Caption Suggestion", caption_prompt)
