# services/social_service.py

from tasks.scheduler import scheduler
from db import get_session
from models import Event
from datetime import datetime
import json

# ----------------------
# Event Logging Helpers
# ----------------------

def log_social_event(event_type: str, payload: dict):
    with get_session() as s:
        e = Event(type=event_type, payload=json.dumps(payload))
        s.add(e)
        s.commit()
    return {"status": "ok", "event_type": event_type}

# ----------------------
# Social Post Management
# ----------------------

# In-memory storage for demo; replace with DB in production
user_posts = {}
user_engagements = {}

def schedule_post(user_id: int, platform: str, content: str, schedule_time: datetime):
    """Schedule a post (in-memory stub)."""
    if user_id not in user_posts:
        user_posts[user_id] = []
    post = {
        "platform": platform,
        "content": content,
        "schedule_time": schedule_time,
        "status": "Scheduled"
    }
    user_posts[user_id].append(post)
    # Optionally schedule with APScheduler
    scheduler.add_job(
        lambda p=platform, c=content: log_social_event("social_publish", {"platform": p, "content": c, "ts": datetime.utcnow().isoformat()}),
        'date',
        run_date=schedule_time
    )
    return post

def publish_now(user_id: int, platform: str, content: str):
    """Publish immediately (stub)."""
    event_payload = {"platform": platform, "content": content, "ts": datetime.utcnow().isoformat()}
    log_social_event("social_publish", event_payload)
    if user_id in user_posts:
        user_posts[user_id].append({**event_payload, "status": "Published"})
    return {"status": "published", "platform": platform}

def get_posts(user_id: int):
    """Get scheduled or published posts for a user."""
    return user_posts.get(user_id, [])

def get_engagements(user_id: int):
    """Return engagement stubs for a user."""
    if user_id not in user_engagements:
        user_engagements[user_id] = [
            {"platform": "Instagram", "comment": "Love this post!", "status": "Unread"},
        ]
    return user_engagements[user_id]

def get_metrics():
    """Aggregate recent social events."""
    with get_session() as s:
        rows = s.exec("SELECT * FROM event ORDER BY created_at DESC LIMIT 200").all()
    return {"events_count": len(rows)}

def reply_comment(platform: str, conversation_id: str, message: str):
    """Record a reply event (stub for platform API)."""
    return log_social_event("social_reply", {
        "platform": platform,
        "conversation_id": conversation_id,
        "message": message,
        "ts": datetime.utcnow().isoformat()
    })

def run_scheduled_posts():
    print("📢 Checking for scheduled posts...")
    # fetch posts due now → post → update status

