import streamlit as st
from services.storage import load_insights

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
