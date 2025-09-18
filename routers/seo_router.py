# routers/seo_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.seo_service import keyword_suggestions, keyword_density, rank_check_stub

router = APIRouter()

class KeywordReq(BaseModel):
    seed: str
    country: str = "in"

class DensityReq(BaseModel):
    text: str
    keyword: str

@router.post("/keyword-research")
def kw_research(req: KeywordReq):
    try:
        return {"success": True, "keywords": keyword_suggestions(req.seed, req.country)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/keyword-density")
def kw_density(req: DensityReq):
    return {"success": True, "density": keyword_density(req.text, req.keyword)}

@router.get("/rank-check")
def rank_check(url: str, keyword: str):
    """
    Very basic stub. For real ranking use SerpAPI or Google Search Console API.
    """
    return {"success": True, "rank_data": rank_check_stub(url, keyword)}
