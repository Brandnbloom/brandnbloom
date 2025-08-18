import streamlit as st, pathlib
from utils.ui import inject_css, dark_mode_toggle, load_branding
from bloominsight.scraper import fetch_public_profile
from ai_tools.bloomscore import compute_bloomscore

inject_css(); dark_mode_toggle()
st.title("🔬 BloomScore")
handle = st.text_input("Instagram handle (without @)", value="brandnbloom_demo")
if st.button("Compute BloomScore"):
    profile = fetch_public_profile(handle)
    res = compute_bloomscore(profile)
    st.metric("BloomScore", res["score"])
    st.write("Bucket:", res["bucket"])
    st.json(res["components"])
    st.write("Recommendations:")
    for r in res["analysis"].get("recommendations", []):
        st.write("•", r)
