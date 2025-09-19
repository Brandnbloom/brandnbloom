# services/social_service.py
from tasks.scheduler import scheduler
from db import get_session
from models import Event
from datetime import datetime
import json

def schedule_post(platform, content, publish_at):
    # parse publish_at into run_date; for demo we schedule immediate (stub)
    def job_func(p, c):
        # real implementation would call platform API
        with get_session() as s:
            e = Event(type="social_publish", payload=json.dumps({"platform":p,"content":c,"ts":datetime.utcnow().isoformat()}))
            s.add(e); s.commit()
    scheduler.add_job(job_func, 'date', args=[platform, content], run_date=publish_at)
    return {"status": "scheduled", "platform": platform, "publish_at": publish_at}

def publish_now(platform, content):
    # call platform publish API (Meta/Twitter) — stub
    with get_session() as s:
        e = Event(type="social_publish", payload=json.dumps({"platform":platform,"content":content,"ts":datetime.utcnow().isoformat()}))
        s.add(e); s.commit()
    return {"status": "published", "platform": platform}

def get_metrics(q):
    # Stub: return local events aggregated; for real data integrate platform APIs or webhook ingestion
    with get_session() as s:
        rows = s.exec("SELECT * FROM event ORDER BY created_at DESC LIMIT 200").all()
        return {"events_count": len(rows)}

def reply_comment(platform, conversation_id, message):
    # Integrate platform API; stub records a reply event
    with get_session() as s:
        e = Event(type="social_reply", payload=json.dumps({"platform":platform,"conversation_id":conversation_id,"message":message,"ts":datetime.utcnow().isoformat()}))
        s.add(e); s.commit()
    return {"status":"ok"}
