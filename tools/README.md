# BloomInsight — Final Package (Playwright scraper + Proxy rotation + Postgres + Docker)

This scaffold includes:
- scraper/ : Playwright-based scraper, login helper, proxy rotation.
- backend/ : Flask API, SQLAlchemy models, CRUD, migration helper.
- streamlit/ : Streamlit dashboard scaffold.
- reports/ : PDF report generator (ReportLab) and chart helpers.
- scheduler/ : APScheduler job examples for daily pulls & weekly email reports.
- docker/ : Dockerfiles and docker-compose for local dev (Postgres + backend + streamlit).
- proxies.txt : sample proxy list (placeholders).
- config_example.py : environment variable template.
- requirements.txt

Important: update config_example.py -> config.py before running. Run `playwright install` once after installing requirements.
