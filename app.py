import streamlit as st

<meta name="google-site-verification" content="YE75SNSAONjr9Y4IYqOZiA1dkG5OYRIstxk-SdSJEZY" />

st.set_page_config(page_title="Brand n Bloom", layout="wide")

# 🌸 Banner
st.image("assets/banner.png", use_container_width=True)

# 🌟 Introduction
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: 600;
        color: #3c3c3c;
    }
    .subtext {
        font-size: 18px;
        color: #666;
    }
</style>

<div class="main-title">Welcome to Brand n Bloom 🌸</div>
<div class="subtext">
    Unleash the power of branding with AI. Our tools empower restaurants and brands to analyze, grow, and bloom creatively.
</div>
""", unsafe_allow_html=True)

# 🌿 Sidebar Navigation
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.markdown("### Navigate")
    
    st.page_link("app.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/BloomScore.py", label="📊 BloomScore")
    st.page_link("pages/Consumer_Behavior.py", label="🧠 DinePsych")
    st.page_link("pages/Visual_Audit.py", label="🎨 Visual Audit")
    st.page_link("pages/Review_Reply.py", label="💬 Review Assistant")
    st.page_link("pages/Digital_Menu.py", label="📄 Digital Menu")
    st.page_link("pages/BloomInsight.py", label="📈 BloomInsight")

    st.markdown("### 📚 Info")
    st.page_link("pages/about_us.py", label="👥 About Us")
    st.page_link("pages/about_ceo.py", label="👩‍💼 About CEO")
    st.page_link("pages/our_services.py", label="🛠️ Products & Services")
    st.page_link("pages/manifesto.py", label="📜 Manifesto")

    st.markdown("### 📝 More")
    st.page_link("pages/blogs.py", label="📝 Blogs")
    st.page_link("pages/contact_us.py", label="📬 Contact")
    st.page_link("pages/legal.py", label="⚖️ Terms & Privacy")
    st.page_link("pages/disclaimer.py", label="🛑 Disclaimer")

import streamlit.components.v1 as components
st.markdown("""
<!-- Google Translate Widget -->
<div id="google_translate_element"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}
</script>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
""", unsafe_allow_html=True)

st.markdown("""
<!--Start of Tawk.to Script-->
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var 
s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/6860e99d73af5e1912a4fcb7/1iut914c9';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
""", unsafe_allow_html=True)


def cookie_consent():
    if "accepted_cookies" not in st.session_state:
        st.session_state.accepted_cookies = False

    if not st.session_state.accepted_cookies:
        with st.expander("🍪 We use cookies! Click to accept."):
            if st.button("Accept Cookies"):
                st.session_state.accepted_cookies = True
                st.success("Thank you for accepting cookies!")

cookie_consent()
st.markdown(
    "<hr><center>© 2025 Brand n Bloom. All Rights Reserved.</center>",
    unsafe_allow_html=True
)

