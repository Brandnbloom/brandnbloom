import streamlit as st
from utils.ui import inject_css, dark_mode_toggle
from ai_tools.influencer_finder import find_influencers

inject_css(); dark_mode_toggle()
st.title("🤝 Influencer Finder")
handles = st.text_area("Candidate handles (comma separated)", "influencer1,influencer2").split(",")
minf = st.number_input("Min followers", value=1000, step=100)
topn = st.number_input("Top N", value=5, step=1)
if st.button("Find"):
    res = find_influencers([h.strip() for h in handles if h.strip()], min_followers=minf, top_n=topn)
    st.json(res)
