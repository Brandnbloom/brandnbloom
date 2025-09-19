# services/keyword_service.py
from db import get_session
from models import Keyword, KeywordRank
from datetime import datetime
from tasks.scheduler import scheduler
import random

def add_keyword(keyword: str, target_url: str=None):
    with get_session() as s:
        k = Keyword(keyword=keyword, target_url=target_url)
        s.add(k); s.commit(); s.refresh(k)
        return {"keyword_id": k.id, "keyword": k.keyword}

def get_keywords():
    with get_session() as s:
        rows = s.exec("SELECT * FROM keyword").all()
        return rows

def _check_ranks_once():
    with get_session() as s:
        kws = s.exec("SELECT * FROM keyword").all()
        for kw in kws:
            # DEMO: simulate rank (replace with SERP API or custom scraper)
            rank = random.randint(1, 100)
            kr = KeywordRank(keyword_id=kw['id'], rank=rank)
            s.add(kr)
        s.commit()

def schedule_daily_rank_check():
    # schedule at midnight daily. For demo schedule every minute (change trigger)
    job = scheduler.add_job(_check_ranks_once, 'interval', minutes=1440, id="daily_keyword_check", replace_existing=True)
    return job.id

def get_keyword_history(keyword_id: int):
    with get_session() as s:
        rows = s.exec(f"SELECT * FROM keywordrank WHERE keyword_id={keyword_id} ORDER BY checked_at DESC LIMIT 365").all()
        return rows
