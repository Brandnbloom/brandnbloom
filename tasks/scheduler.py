# tasks/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import os
import atexit

# -----------------------------
#  IMPORT YOUR SERVICES
# -----------------------------
from services.keyword_service import schedule_daily_rank_check
from services.social_service import run_scheduled_posts
from services.seo_service import run_scheduled_seo_audit

# -----------------------------
#  PREVENT MULTIPLE SCHEDULERS
# -----------------------------
# Render/Gunicorn spawns multiple workers → prevents duplication
if os.environ.get("RUN_MAIN") != "true":
    print("⚠️ Scheduler not started because this is not the main thread.")
else:
    print("🚀 Scheduler starting...")

    scheduler = BackgroundScheduler()

    # -----------------------------
    #  JOB 1 — HEARTBEAT (Every hour)
    # -----------------------------
    def heartbeat():
        print("⏱ Scheduler heartbeat:", datetime.utcnow().isoformat())

    scheduler.add_job(
        heartbeat,
        trigger=CronTrigger(minute="0"),  # every hour at :00
        id="heartbeat",
        replace_existing=True,
    )

    # -----------------------------
    #  JOB 2 — Daily Keyword Rank Check (Every day at 06:00)
    # -----------------------------
    scheduler.add_job(
        schedule_daily_rank_check,
        trigger=CronTrigger(hour=6, minute=0),
        id="daily_keyword_rank_check",
        replace_existing=True,
    )

    # -----------------------------
    #  JOB 3 — Run Scheduled Social Posts (Every minute)
    # -----------------------------
    scheduler.add_job(
        run_scheduled_posts,
        trigger=CronTrigger(second="0"),  # every minute
        id="scheduled_social_posts",
        replace_existing=True,
    )

    # -----------------------------
    #  JOB 4 — Weekly SEO Audit (Every Monday at 7 AM)
    # -----------------------------
    scheduler.add_job(
        run_scheduled_seo_audit,
        trigger=CronTrigger(day_of_week="mon", hour=7, minute=0),
        id="weekly_seo_audit",
        replace_existing=True,
    )

    # Start the scheduler
    scheduler.start()
    print("✅ Scheduler started successfully.")

    # Shutdown cleanly
    atexit.register(lambda: scheduler.shutdown())
