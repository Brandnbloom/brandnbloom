# tasks/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import atexit

scheduler = BackgroundScheduler()
scheduler.start()

# Example job - placeholder, you can import services.keyword_service.schedule_daily_rank_check to add jobs
def health_job():
    print("scheduler heartbeat:", datetime.utcnow().isoformat())

scheduler.add_job(health_job, IntervalTrigger(minutes=60), id="heartbeat", replace_existing=True)

atexit.register(lambda: scheduler.shutdown())
