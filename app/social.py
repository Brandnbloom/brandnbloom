from fastapi import APIRouter, Depends, HTTPException
from fastapi import Header
from .utils.jwt_helper import decode_access_token
from .database import get_db

router = APIRouter()

# In-memory storage for simulation
user_posts = {}
user_engagements = {}

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["user_id"]

# ---------------- Post Scheduler ----------------
@router.post("/schedule-post")
def schedule_post(platform: str, content: str, schedule_time: str, user_id: int = Depends(get_current_user)):
    """
    Schedule a post for a user
    """
    if user_id not in user_posts:
        user_posts[user_id] = []
    post = {"platform": platform, "content": content, "schedule_time": schedule_time, "status": "Scheduled"}
    user_posts[user_id].append(post)
    return {"status": "Post scheduled", "post": post}

@router.get("/posts")
def get_posts(user_id: int = Depends(get_current_user)):
    """
    Retrieve all posts for the user
    """
    return user_posts.get(user_id, [])

# ---------------- Engagement API ----------------
@router.get("/engagements")
def get_engagements(user_id: int = Depends(get_current_user)):
    """
    Simulated engagement metrics (comments/likes)
    """
    if user_id not in user_engagements:
        user_engagements[user_id] = [
            {"platform": "Instagram", "comment": "Love this post!", "status": "Unread"},
            {"platform": "LinkedIn", "comment": "Very informative.", "status": "Unread"}
        ]
    return user_engagements[user_id]

@router.post("/reply-comment")
def reply_comment(platform: str, comment_id: int, reply: str, user_id: int = Depends(get_current_user)):
    """
    Reply to a comment (simulated)
    """
    engagements = user_engagements.get(user_id, [])
    if comment_id < 0 or comment_id >= len(engagements):
        raise HTTPException(status_code=404, detail="Comment not found")
    engagements[comment_id]["reply"] = reply
    engagements[comment_id]["status"] = "Replied"
    return {"status": "Replied", "engagement": engagements[comment_id]}
