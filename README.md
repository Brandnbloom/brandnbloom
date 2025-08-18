# Brand N Bloom — AI-Powered Marketing Platform (Streamlit + Render)

This is a production-ready **MVP scaffold** covering:
- Python + Streamlit multipage web app
- Secure auth (signup/login with hashed passwords + JWT helpers)
- SQLite data logging + historical tracking
- BloomInsight (Instagram analysis) with **custom scraper placeholders** + fallbacks
- KPI dashboards (mock + real-ready)
- Weekly **PDF Report** generation (ReportLab) + **Email delivery** (SMTP / MailerLite-ready)
- APScheduler-based tasks (+ Render Cron alternative)
- Modular AI tools (caption/hashtag generator, audit tools, etc., with OpenAI pluggable)
- Deployment on **Render** with `render.yaml`

> ⚠️ Instagram's public HTML and endpoints change often. This repo provides a **Custom Scraper API** stub and a **fallback mock** so your app works end-to-end even without live scrape access. Swap in your working scraper in `bloominsight/scraper.py`.

---

## Local Quickstart

```bash
# 1) Create & activate venv (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Create .env (see .env.example)
cp .env.example .env
# Fill in OPENAI_API_KEY, SMTP creds, etc.

# 4) Initialize DB
python tools/init_db.py

# 5) Run Streamlit app
streamlit run streamlit_app.py
```

Open: http://localhost:8501

Default pages: Home, Features, Pricing, Blog, Dashboard, Contact, About, Login, Signup.

---

## Render Deployment

1. Push this repo to GitHub.
2. On Render, create a **Web Service**:
   - Runtime: Python 3.12+
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
3. Add **Environment Variables** (Render Dashboard → Environment):
   - `OPENAI_API_KEY` *(optional, for AI features)*
   - `JWT_SECRET` *(required, any random string)*
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`
   - `MAILERLITE_API_KEY` *(optional)*
   - `BASE_URL` *(your service URL, used in links/reports)*
4. (Optional) **Cron Job** on Render to send weekly reports:
   - Make a second Web Service from `api_server.py` (FastAPI endpoints), or
   - Create a **Cron Job** that runs: `python tools/run_weekly_reports.py`

> Using two services: one for the Streamlit UI, one for the API/scheduler, is a clean separation for scale.

---

## Structure

```
brand-n-bloom/
├─ streamlit_app.py                # Entrypoint (Home page)
├─ pages/
│  ├─ 01_🏠_Home.py
│  ├─ 02_✨_Features.py
│  ├─ 03_💰_Pricing.py
│  ├─ 04_📰_Blog.py
│  ├─ 05_📊_Dashboard.py
│  ├─ 06_📨_Contact.py
│  ├─ 07_ℹ️_About.py
│  ├─ 08_🔐_Login.py
│  └─ 09_🆕_Signup.py
├─ bloominsight/
│  ├─ __init__.py
│  ├─ scraper.py                   # Custom Instagram scraper (stub + fallback)
│  ├─ analyzer.py                  # KPIs, ER, hashtag/caption suggestions
│  ├─ report_api.py                # PDF pipeline & weekly email
│  └─ utils.py
├─ ai_tools/
│  ├─ __init__.py
│  ├─ caption_generator.py
│  ├─ hashtag_recommender.py
│  ├─ prompts.py
│  └─ audit_tools.py
├─ auth/
│  ├─ __init__.py
│  ├─ jwt_utils.py
│  ├─ security.py
│  └─ session.py
├─ data/
│  ├─ schema.sql
│  └─ sample_instagram.json
├─ db/
│  ├─ __init__.py
│  ├─ db.py
│  └─ models.py
├─ emailer/
│  ├─ __init__.py
│  └─ mailer.py
├─ scheduler/
│  ├─ __init__.py
│  └─ scheduler.py
├─ tools/
│  ├─ init_db.py
│  └─ run_weekly_reports.py
├─ utils/
│  ├─ charts.py
│  └─ pdf.py
├─ api_server.py                   # Optional FastAPI for background tasks
├─ requirements.txt
├─ render.yaml
├─ .streamlit/config.toml
├─ .env.example
└─ .gitignore
```

---

## Notes

- **Auth**: Passwords are hashed (bcrypt). JWT helpers allow stateless auth if you decide to expose APIs later. Streamlit session is used for UI-session.
- **SEO**: Streamlit is SPA-like. Use `st.set_page_config`, meta description, and fast-loading assets. Consider a static marketing site (Next.js) fronting this for advanced SEO.
- **PDF**: `utils/pdf.py` uses ReportLab → lightweight and Render-friendly.
- **Scheduler**: APScheduler works in-process; on Render, prefer a Cron Job or separate worker for reliability.
- **Scraper**: Replace stubs in `bloominsight/scraper.py` with your working implementation.
- **OpenAI** features are guarded by env checks, so the app runs without keys.

---

## Instagram Scraper (Playwright)

This project includes a **live** Playwright scraper with proxy support and a safe **fallback**.

### Enable live scraping
Set environment variable:
```
IG_SCRAPER_MODE=live
```
Optional proxy:
```
PROXY_SERVER=http://host:port
PROXY_USERNAME=youruser
PROXY_PASSWORD=yourpass
```

### One-time install
After installing requirements, run:
```
python -m playwright install chromium
```

> If scraping fails (rate limits/cookies/layout changes), the app automatically falls back to demo data so dashboards remain usable.

## Production steps (Playwright + Render)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers (required for live scraping):
   ```bash
   python -m playwright install chromium
   ```

3. Set environment variables (Render Dashboard or .env):
   - `JWT_SECRET` - random string
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`
   - `IG_SCRAPER_MODE=live` (or `fallback`)
   - `PROXY_SERVER` (optional), `PROXY_USERNAME`, `PROXY_PASSWORD`
   - `OPENAI_API_KEY` (optional)
   - `DATABASE_URL` (e.g., sqlite:///bnb.sqlite3 or Postgres URL)
   - `BASE_URL` (your app URL)

4. On Render:
   - Create two services: `brand-n-bloom-app` (Streamlit) and `brand-n-bloom-api` (Flask).
   - For the Flask service set start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - For Streamlit start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
   - Add a Cron Job or Scheduled Job to call `/send-report` per user weekly (or run `python tools/run_weekly_reports.py` as a cron script).

5. Database:
   - For production, use Postgres (Render Postgres addon) and set `DATABASE_URL` accordingly. Update `db/db.py` to use SQLAlchemy/Postgres if needed.

6. Logs & Monitoring:
   - Enable Render logs for both services. For Playwright scraping errors, ensure proxy and rate-limiting are configured.

---

## Additional tools included in this build (ready-to-use stubs)

- BloomScore (ai_tools/bloomscore.py) — combined brand health scoring.
- Consumer Behavior Analysis (ai_tools/consumer_behavior.py) — questionnaire engine.
- Automated Email Marketing (emailer/mailer and emailer/mailerlite_adapter) — SMTP + MailerLite adapter.
- Influencer Finder (ai_tools/influencer_finder.py) — rank handles by ER & followers.
- Business Comparison (ai_tools/business_compare.py) — compare key metrics across handles.
- Menu Pricing Optimization (ai_tools/menu_pricing.py) — pricing suggestions based on cost & margin.
- Customer Loyalty AI (ai_tools/loyalty.py) — simple points-to-rewards engine.

These modules are rule-based and ready to replace with ML-backed logic as you scale.
