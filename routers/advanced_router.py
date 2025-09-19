# routers/advanced_router.py
from fastapi import APIRouter
from services.internal_service import recommend_content, start_cro_test, ecommerce_sync, register_affiliate

router = APIRouter()

@router.post("/personalization")
def personalization(q: dict):
    return recommend_content(q)

@router.post("/cro/start")
def cro_start(q: dict):
    return start_cro_test(q)

@router.post("/ecommerce/sync")
def ecommerce_sync_endpoint(q: dict):
    return ecommerce_sync(q)

@router.post("/affiliate/register")
def affiliate_register(q: dict):
    return register_affiliate(q)
