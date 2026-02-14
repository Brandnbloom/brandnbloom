import os
import streamlit as st
import streamlit.components.v1 as components
import threading
from flask import Flask, request, jsonify
from bloominsight.scraper import fetch_public_profile
from bloominsight.analyzer import analyze_profile
from ai_tools.bloomscore import compute_bloomscore
from ai_tools.influencer_finder import find_influencers
from ai_tools.business_compare import compare_handles
from ai_tools.menu_pricing import suggest_prices
from ai_tools.consumer_behavior import run_questionnaire
from bloominsight.report_api import generate_and_send_weekly_report
from db.models import log_kpis, save_report
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

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"ok": True, "mode": os.environ.get("IG_SCRAPER_MODE","fallback")})

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json() or {}
    handle = data.get('handle')
    if not handle:
        return jsonify({"error": "missing handle"}), 400
    profile = fetch_public_profile(handle)
    return jsonify(profile)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json() or {}
    handle = data.get('handle')
    if not handle:
        return jsonify({"error": "missing handle"}), 400
    profile = fetch_public_profile(handle)
    analysis = analyze_profile(profile)
    # Log KPIs
    try:
        log_kpis(handle, analysis['followers'], analysis['likes'], analysis['reach'], analysis['impressions'], analysis['engagement_rate'])
    except Exception as e:
        app.logger.debug("DB log error: %s", e)
    return jsonify(analysis)

@app.route('/send-report', methods=['POST'])
def send_report():
    data = request.get_json() or {}
    handle = data.get('handle')
    to_email = data.get('email')
    user_id = data.get('user_id', 1)
    if not handle or not to_email:
        return jsonify({"error":"missing handle or email"}), 400
    profile = fetch_public_profile(handle)
    analysis = analyze_profile(profile)
    kpis = {
        "Followers": analysis["followers"],
        "Likes": analysis["likes"],
        "Reach": analysis["reach"],
        "Impressions": analysis["impressions"],
        "Engagement Rate (%)": analysis["engagement_rate"],
    }
    pdf = generate_and_send_weekly_report(user_id, to_email, handle, kpis)
    return jsonify({"status":"sent", "pdf": pdf})

@app.route('/compare', methods=['POST'])
@app.route('/bloomscore', methods=['POST'])
def bloomscore_api():
    data = request.get_json() or {}
    handle = data.get('handle')
    if not handle:
        return jsonify({'error':'missing handle'}),400
    p = fetch_public_profile(handle)
    return jsonify(compute_bloomscore(p))

@app.route('/influencers', methods=['POST'])
def influencers_api():
    data = request.get_json() or {}
    handles = data.get('handles', [])
    return jsonify(find_influencers(handles))

@app.route('/menu-suggest', methods=['POST'])
def menu_suggest_api():
    data = request.get_json() or {}
    cost = float(data.get('cost',0))
    margin = float(data.get('margin',40))
    comp = data.get('competitor')
    comp = float(comp) if comp else None
    return jsonify(suggest_prices(cost, margin, comp))

@app.route('/consumer', methods=['POST'])
def consumer_api():
    data = request.get_json() or {}
    answers = data.get('answers',{})
    return jsonify(run_questionnaire(answers))

@app.route('/influencer-find', methods=['POST'])
def influencer_find_api():
    data = request.get_json() or {}
    handles = data.get('handles',[])
    return jsonify(find_influencers(handles))

def compare():
    data = request.get_json() or {}
    handles = data.get('handles', [])
    if not handles or not isinstance(handles, list):
        return jsonify({"error":"missing handles list"}), 400
    results = {}
    for h in handles:
        try:
            p = fetch_public_profile(h)
            a = analyze_profile(p)
            results[h] = {"followers": a["followers"], "engagement_rate": a["engagement_rate"]}
        except Exception as e:
            results[h] = {"error": str(e)}
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

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
