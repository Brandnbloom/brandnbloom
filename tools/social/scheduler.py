from apscheduler.schedulers.background import BackgroundScheduler
import time
from tools.social.post_worker import post_to_platform

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_post(platform, content, post_time, meta):
    job = scheduler.add_job(post_to_platform, 'date', run_date=post_time, args=[platform, content, meta])
    return job.id

# simple worker function
def post_to_platform(platform, content, meta):
    # For now, just log; later integrate official platform APIs (Meta Graph API, X/Twitter API)
    print(f"Posting to {platform} at {time.ctime()} content: {content[:50]}")
