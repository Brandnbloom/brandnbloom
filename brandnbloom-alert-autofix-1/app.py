import os
import streamlit as st
import streamlit.components.v1 as components
import threading
from utils_sitemap import update_sitemap_and_ping  # NEW import

# ================= Run sitemap in background =================
threading.Thread(target=update_sitemap_and_ping, daemon=True).start()
# =============================================================

# Page settings
st.set_page_config(page_title="Brand n Bloom", layout="wide")

# --- PWA + Meta tags ---
st.markdown("""
<link rel="manifest" href="static/manifest.json" />
<meta name="theme-color" content="#FF2898" />
<link rel="apple-touch-icon" href="static/icon-192.png">
<link rel="icon" href="static/favicon.ico" type="image/x-icon">
<meta name="google-site-verification" content="YE75SNSAONjr9Y4IYqOZiA1dkG5OYRIstxk-SdSJEZY" />
""", unsafe_allow_html=True)

# --- Service Worker Registration ---
components.html("""
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("static/service-worker.js")
      .then((reg) => console.log("✅ SW registered", reg))
      .catch((err) => console.error("❌ SW registration failed", err));
  });
}
</script>
""", height=0)

# Banner
st.image("assets/banner.png", use_column_width=True)

# Welcome text
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

# --- Collapsible Menu ---
with st.expander("📂 Click here to explore all tools and info sections"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.page_link("pages/BloomScore.py", label="📊 BloomScore")
        st.page_link("pages/Consumer_Behavior.py", label="🧠 DinePsych")
        st.page_link("pages/Visual_Audit.py", label="🎨 Visual Audit")
        st.page_link("pages/Review_Reply.py", label="💬 Review Assistant")

    with col2:
        st.page_link("pages/Digital_Menu.py", label="📄 Digital Menu")
        st.page_link("pages/BloomInsight.py", label="📈 BloomInsight")
        st.page_link("pages/blogs.py", label="📝 Blogs")
        st.page_link("pages/contact_us.py", label="📬 Contact")

    with col3:
        st.page_link("pages/about_us.py", label="👥 About Us")
        st.page_link("pages/about_ceo.py", label="👩‍💼 About CEO")
        st.page_link("pages/our_services.py", label="🛠️ Our Services")
        st.page_link("pages/manifesto.py", label="📜 Manifesto")
        st.page_link("pages/legal.py", label="⚖️ Terms & Privacy")
        st.page_link("pages/disclaimer.py", label="🛑 Disclaimer")

# --- BloomInsight Section ---
st.markdown("## 📈 BloomInsight - Instagram Analytics")

username = st.text_input("Enter Instagram Username")
if st.button("Analyze"):
    if username:
        profile_data = scrape_instagram_profile(username)
        if profile_data:
            insights = analyze_profile(profile_data)
            render_dashboard(profile_data, insights)
        else:
            st.error("Could not fetch Instagram profile. Try again or check proxies.")
    else:
        st.warning("Please enter a username.")

# --- Google Translate ---
components.html("""
<div id="google_translate_element"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}
</script>
<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
""", height=60)

# --- Tawk.to Live Chat ---
components.html("""
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/6860e99d73af5e1912a4fcb7/1iut914c9';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
""", height=0)

# --- Cookie Consent ---
def cookie_consent():
    if "accepted_cookies" not in st.session_state:
        st.session_state.accepted_cookies = False

    if not st.session_state.accepted_cookies:
        with st.expander("🍪 We use cookies! Click to accept."):
            if st.button("Accept Cookies"):
                st.session_state.accepted_cookies = True
                st.success("Thank you for accepting cookies!")

cookie_consent()

# --- Google Analytics ---
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0GBTQZDD53"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-0GBTQZDD53');
</script>
""", height=0)

# Footer
st.markdown("""
<hr>
<p style='text-align: center; font-size: 0.9em;'>© 2025 Brand n Bloom. All rights reserved.</p>
""", unsafe_allow_html=True)
