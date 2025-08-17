# Copy to config.py and fill values
DATABASE_URL = "postgresql://bloom:bloom_pass@db:5432/bloominsight"
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "you@example.com"
SMTP_PASS = "password"
FROM_EMAIL = "reports@brand-n-bloom.com"
ADMIN_EMAILS = ["client@example.com"]
STORAGE_STATE_PATH = "scraper/storage_state.json"
PROXY_LIST_FILE = "proxies.txt"
DAILY_PULL_CRON_HOUR_UTC = 2
