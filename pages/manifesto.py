import streamlit as st

st.set_page_config(page_title="Our Manifesto - Brand n Bloom", layout="centered")

# 🌸 Title
st.title("📜 Our Manifesto")

# 🌿 Manifesto Content
st.markdown("""
<style>
.manifesto {
    font-size: 18px;
    line-height: 1.6;
    color: #3c3c3c;
    background-color: #f8f4f2;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    font-family: 'Georgia', serif;
}
</style>

<div class="manifesto">
    In today’s disconnected digital world, we want to bring <strong>empathy</strong> back into how businesses and communities connect online.<br><br>

    Through <strong>Brand n Bloom</strong>, we help restaurants of all types — from small independents to top-tier — improve their <strong>Google rankings</strong> and <strong>search traffic</strong>, so they can attract more real customers and grow.<br><br>

    Our mission is to <strong>humanize SEO</strong> — not just rankings, but <strong>relationships</strong> — helping restaurants thrive with <strong>visibility, connection, and trust</strong>.
</div>
""", unsafe_allow_html=True)

# 🌸 Footer
st.markdown("<br><center>🌼 Thank you for believing in our purpose.</center>", unsafe_allow_html=True)
