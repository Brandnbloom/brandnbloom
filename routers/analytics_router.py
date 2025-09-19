# routers/analytics_router.py
from fastapi import APIRouter
from services.analytics_service import aggregate_metrics, generate_report, list_alerts, create_alert

router = APIRouter()

@router.get("/aggregate")
def aggregate(q: dict = {}):
    return aggregate_metrics(q)

@router.post("/report")
def report(q: dict):
    # q may include date range, format
    return generate_report(q)

@router.get("/alerts")
def alerts():
    return list_alerts()

@router.post("/alerts")
def create(q: dict):
    return create_alert(q)
