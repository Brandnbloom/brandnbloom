import streamlit as st

st.set_page_config(page_title="About the Founder - Brand n Bloom", layout="centered")

# 🌸 Title
st.title("👩‍💼 About the Founder")

# 🌼 Founder Bio Content
st.markdown("""
<style>
.about-box {
    background-color: #f9f6f2;
    padding: 25px;
    border-radius: 12px;
    font-size: 17px;
    line-height: 1.7;
    color: #333;
    font-family: 'Georgia', serif;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.quote {
    font-style: italic;
    color: #777;
    border-left: 4px solid #d8a1c4;
    padding-left: 12px;
    margin-top: 20px;
}
</style>

<div class="about-box">
    <strong>Shreya Anaokar</strong> is the heart behind <strong>Brand n Bloom</strong>. With over 4 years of experience in finance content, digital strategy, and creative branding, she blends analytical thinking with emotional intelligence to help restaurants and small businesses thrive online.<br><br>

    Born from grit and grace, Brand n Bloom is Shreya’s vision to <strong>humanize SEO</strong> — making visibility not just about rankings, but about <strong>real, meaningful connections</strong>.<br><br>

    Inspired by her daughter <strong>Yathvika</strong>, this journey is not just business — it’s about <strong>legacy building</strong> and creating impact through authenticity.
    
    <div class="quote">
        “I don’t just build brands — I nurture them like my own dreams.”
    </div>
</div>
""", unsafe_allow_html=True)
