# app/social.py

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Dict, List
from .utils.jwt_helper import decode_access_token

router = APIRouter()

# -------------------------------------------------------------------
# Auth Helper
# -------------------------------------------------------------------
def get_current_user(authorization: str = Header(...)):
    """
    Extract Bearer token and validate JWT.
    """
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Authorization header malformed")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload["user_id"]


# -------------------------------------------------------------------
# In-memory storage (replace with DB later)
# -------------------------------------------------------------------
user_posts: Dict[int, List[dict]] = {}
user_engagements: Dict[int, List[dict]] = {}


# -------------------------------------------------------------------
# Pydantic Models
# -------------------------------------------------------------------
class SchedulePostRequest(BaseModel):
    platform: str = Field(..., description="Instagram / LinkedIn / YouTube")
    content: str = Field(..., min_length=3)
    schedule_time: str = Field(..., description="ISO timestamp or human format")


class ReplyRequest(BaseModel):
    platform: str
    comment_id: int
    reply: str = Field(..., min_length=1)


# -------------------------------------------------------------------
# Post Scheduler
# -------------------------------------------------------------------
@router.post("/schedule-post")
def schedule_post(
    data: SchedulePostRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Schedule a new post for the user's social accounts.
    """

    user_posts.setdefault(user_id, [])

    post_id = len(user_posts[user_id])

    post = {
        "id": post_id,
        "platform": data.platform,
        "content": data.content,
        "schedule_time": data.schedule_time,
        "status": "Scheduled"
    }

    user_posts[user_id].append(post)

    return {
        "status": "Post scheduled",
        "post": post
    }


@router.get("/posts")
def get_posts(user_id: int = Depends(get_current_user)):
    """
    Retrieve all scheduled posts for the user.
    """
    return {
        "status": "success",
        "posts": user_posts.get(user_id, [])
    }


# -------------------------------------------------------------------
# Engagement API
# -------------------------------------------------------------------
@router.get("/engagements")
def get_engagements(user_id: int = Depends(get_current_user)):
    """
    Returns simulated engagement: comments, likes, mentions, etc.
    """
    # First-time response: populate dummy data
    if user_id not in user_engagements:
        user_engagements[user_id] = [
            {"id": 0, "platform": "Instagram", "comment": "Love this post!", "status": "Unread"},
            {"id": 1, "platform": "LinkedIn", "comment": "Very informative.", "status": "Unread"}
        ]

    return {
        "status": "success",
        "engagements": user_engagements[user_id]
    }


# -------------------------------------------------------------------
# Reply to Comment
# -------------------------------------------------------------------
@router.post("/reply-comment")
def reply_comment(
    data: ReplyRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Reply to a comment on any platform (simulated).
    """

    engagements = user_engagements.get(user_id, [])

    if data.comment_id < 0 or data.comment_id >= len(engagements):
        raise HTTPException(status_code=404, detail="Comment not found")

    engagements[data.comment_id]["reply"] = data.reply
    engagements[data.comment_id]["status"] = "Replied"

    return {
        "status": "success",
        "engagement": engagements[data.comment_id]
    }
