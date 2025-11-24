from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from tools.social.post_worker import post_to_platform
import sqlite3
import json
import datetime
import time

DB = "scheduler.db"

# -------------------------------------------------------------------
# DB INIT
# -------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS scheduled_posts (
        id TEXT PRIMARY KEY,
        platform TEXT,
        content TEXT,
        run_time TEXT,
        repeat TEXT,
        meta TEXT,
        status TEXT DEFAULT 'scheduled',
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------------------------------------------------
# APScheduler
# -------------------------------------------------------------------
scheduler = BackgroundScheduler()
scheduler.start()

# -------------------------------------------------------------------
# Save Job in DB
# -------------------------------------------------------------------
def save_job(job_id, platform, content, run_time, repeat, meta):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO scheduled_posts 
        (id, platform, content, run_time, repeat, meta, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job_id,
        platform,
        content,
        run_time,
        repeat,
        json.dumps(meta),
        "scheduled",
        datetime.datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

# -------------------------------------------------------------------
# Update job status
# -------------------------------------------------------------------
def update_status(job_id, status):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE scheduled_posts SET status=? WHERE id=?", (status, job_id))
    conn.commit()
    conn.close()

# -------------------------------------------------------------------
# POST EXECUTION WRAPPER
# -------------------------------------------------------------------
def job_wrapper(platform, content, meta, job_id):
    update_status(job_id, "running")

    try:
        # Actual posting action
        post_to_platform(platform, content, meta)
        update_status(job_id, "completed")
    except Exception as e:
        update_status(job_id, f"failed: {str(e)}")

# -------------------------------------------------------------------
# RECURRING JOB HANDLER
# -------------------------------------------------------------------
def create_trigger(run_time, repeat):
    dt = datetime.datetime.fromisoformat(run_time)

    if repeat == "Daily":
        return CronTrigger(hour=dt.hour, minute=dt.minute)

    if repeat == "Weekly":
        return CronTrigger(day_of_week=dt.weekday(), hour=dt.hour, minute=dt.minute)

    # Default: one-time post
    return DateTrigger(run_date=dt)

# -------------------------------------------------------------------
# MAIN SCHEDULER FUNCTION
# -------------------------------------------------------------------
def schedule_post(platform, content, run_time, meta):
    repeat = meta.get("repeat", "No repeat")

    trigger = create_trigger(run_time, repeat)

    job = scheduler.add_job(
        job_wrapper,
        trigger,
        args=[platform, content, meta, None],  # job_id is added after creation
    )

    # Inject job_id after APScheduler creates it
    job.modify(args=[platform, content, meta, job.id])

    # Save job in database
    save_job(job.id, platform, content, run_time, repeat, meta)

    return job.id

# -------------------------------------------------------------------
# FETCH SCHEDULED POSTS (for dashboard/future UI)
# -------------------------------------------------------------------
def get_scheduled_posts(limit=100):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT id, platform, content, run_time, repeat, meta, status, created_at
        FROM scheduled_posts
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "platform": r[1],
            "content": r[2],
            "run_time": r[3],
            "repeat": r[4],
            "meta": json.loads(r[5]),
            "status": r[6],
            "created_at": r[7],
        })

    return result
