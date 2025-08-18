import streamlit as st
from utils.ui import inject_css, dark_mode_toggle
from ai_tools.consumer_behavior import QUESTIONS, run_questionnaire

inject_css(); dark_mode_toggle()
st.title("🧠 Consumer Behavior Analysis")

st.write("Answer a few quick questions:")
answers = {}
for q in QUESTIONS:
    if q["type"]=="text":
        answers[q["id"]] = st.text_input(q["q"])
    elif q["type"]=="choice":
        answers[q["id"]] = st.selectbox(q["q"], q["choices"])
if st.button("Analyze"):
    out = run_questionnaire(answers)
    st.json(out)
