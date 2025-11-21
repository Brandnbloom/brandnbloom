# services/keyword_service.py

from db import get_session
from models import Keyword, KeywordRank
from datetime import datetime
from tasks.scheduler import scheduler
import random


def add_keyword(keyword: str, target_url: str = None):
    """
    Add a new keyword for rank tracking.
    """
    with get_session() as s:
        k = Keyword(keyword=keyword, target_url=target_url)
        s.add(k)
        s.commit()
        s.refresh(k)
        return {"keyword_id": k.id, "keyword": k.keyword}


def get_keywords():
    """
    Return all tracked keywords.
    """
    with get_session() as s:
        return s.query(Keyword).all()


def _check_ranks_once():
    """
    Simulate a SERP rank check for demo.
    Replace this with actual SERP API integration.
    """
    with get_session() as s:
        keywords = s.query(Keyword).all()

        for kw in keywords:
            simulated_rank = random.randint(1, 100)

            rank_entry = KeywordRank(
                keyword_id=kw.id,
                rank=simulated_rank,
                checked_at=datetime.utcnow()
            )

            s.add(rank_entry)

        s.commit()


def schedule_daily_rank_check():
    """
    Schedule a daily keyword rank check.
    (Current: every 1440 minutes = 1 day)
    """
    job = scheduler.add_job(
        _check_ranks_once,
        "interval",
        minutes=1440,
        id="daily_keyword_check",
        replace_existing=True
    )
    return job.id


def get_keyword_history(keyword_id: int):
    """
    Return latest 365 rank logs for a given keyword.
    """
    with get_session() as s:
        return (
            s.query(KeywordRank)
             .filter(KeywordRank.keyword_id == keyword_id)
             .order_by(KeywordRank.checked_at.desc())
             .limit(365)
             .all()
        )

def schedule_daily_rank_check():
    print("🔍 Running daily keyword rank check...")
    # your keyword rank logic

