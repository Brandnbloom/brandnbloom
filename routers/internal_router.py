# routers/internal_router.py
from fastapi import APIRouter
from services.internal_service import create_task, list_tasks

router = APIRouter()

@router.post("/task")
def create_task(q: dict):
    return create_task(q)

@router.get("/tasks")
def tasks():
    return list_tasks()
