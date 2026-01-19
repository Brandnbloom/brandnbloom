import streamlit as st

from utils.ui import inject_css, dark_mode_toggle, card, page_container
from ai_tools.registry import get_available_tools, run_tool

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Brand n Bloom",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_css()
dark_mode_toggle()

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.image("assets/banner.png", use_container_width=True)

st.markdown(
    """
    <h1 style="text-align:center;">🌸 Brand n Bloom</h1>
    <p style="text-align:center; font-size:18px;">
    AI-powered growth tools for modern brands
    </p>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# HOME
# -------------------------------------------------
if st.session_state.page == "Home":
    with page_container():
        st.markdown("## 🧰 Tools")

        TOOLS = get_available_tools()
        cols = st.columns(3)

        for i, (tool, desc) in enumerate(TOOLS.items()):
            with cols[i % 3]:
                if st.button(tool, use_container_width=True):
                    st.session_state.page = tool
                card(desc)

# -------------------------------------------------
# BLOOMSCORE
# -------------------------------------------------
elif st.session_state.page == "BloomScore":
    with page_container():
        st.markdown("## 🔬 BloomScore")
        st.markdown("Instant analysis of your brand’s social health.")

        handle = st.text_input("Instagram handle (without @)", "brandnbloom")

        if st.button("Compute BloomScore"):
            result = run_tool("BloomScore", {"handle": handle})

            st.metric("BloomScore", result["score"])
            st.write("### Category:", result["bucket"])

            st.markdown("### Score Breakdown")
            st.json(result["components"])

            st.markdown("### Recommendations")
            for r in result["analysis"]["recommendations"]:
                st.write("•", r)

# -------------------------------------------------
# GENERIC TOOL HANDLER (SAFE FALLBACK)
# -------------------------------------------------
else:
    with page_container():
        st.markdown(f"## 🔧 {st.session_state.page}")
        st.info("This tool UI is coming soon.")

        try:
            result = run_tool(st.session_state.page, {})
            st.json(result)
        except Exception:
            st.warning("Tool engine ready. UI will be added next.")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:14px;">
    © 2026 Brand n Bloom • Built with ❤️
    </p>
    """,
    unsafe_allow_html=True
)
