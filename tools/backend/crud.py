from backend.db import SessionLocal, Account, Post
from datetime import datetime
import json

def upsert_account(handle, meta):
    db = SessionLocal()
    acc = db.query(Account).filter(Account.handle==handle).first()
    if not acc:
        acc = Account(handle=handle)
    acc.display_name = meta.get('full_name') or meta.get('display_name')
    acc.bio = meta.get('biography') or meta.get('bio')
    acc.followers = meta.get('followers')
    acc.following = meta.get('following')
    acc.profile_pic_url = meta.get('profile_pic_url')
    acc.last_pull = datetime.utcnow()
    db.add(acc)
    db.commit()
    db.refresh(acc)
    acc_id = acc.id
    db.close()
    return acc_id

def insert_posts(account_id, posts):
    db = SessionLocal()
    for p in posts:
        post_id = p.get('id') or p.get('shortcode')
        exists = db.query(Post).filter(Post.post_id==post_id, Post.account_id==account_id).first()
        if exists:
            continue
        p_obj = Post(account_id=account_id, post_id=post_id, timestamp=datetime.utcfromtimestamp(p.get('timestamp')) if p.get('timestamp') else None,
                     caption=p.get('caption'), like_count=p.get('likes'), comment_count=p.get('comments'),
                     impressions=p.get('impressions'), reach=p.get('reach'), hashtags=None, media_type=None, raw=json.dumps(p))
        db.add(p_obj)
    db.commit()
    db.close()
