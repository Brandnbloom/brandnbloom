# BloomInsight - Instagram Scraper & Analytics (Scaffold)

This repository contains a production-ready scaffold for **BloomInsight**:
- Flask-based Instagram Scraper API (`api.py`)
- Streamlit dashboard (`app.py`) to view KPIs, trends, and recommendations
- SQLite-based historical logging (`db.py`)
- Scheduler for daily pulls & weekly PDF report email (`scheduler.py`)
- Analytics modules for KPI calculation, brand health score, caption recommendations, and alerts (`analytics.py`, `kpi.py`, `nlp_utils.py`)
- Report generator to export weekly PDF audits (`report_generator.py`)
- Sample data and scripts for local testing.

**Important notes**
1. Instagram actively changes scraping endpoints and rate-limits. Prefer using the official Instagram Graph API where possible.
2. This scaffold includes a lightweight public-page scraper fallback. For large-scale or authenticated access, integrate Facebook Graph API or a headless-browser approach (Selenium).
3. Fill in configuration (SMTP credentials, API keys) in `config_example.py`.
4. Run `pip install -r requirements.txt`.

