# routers/writer_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.writer_service import generate_seo_article, paraphrase_text, grammar_check, ai_detect, humanize_text

router = APIRouter()

class GenerateRequest(BaseModel):
    title: str
    keywords: list[str] = []
    length: int = 600  # approximate words

class ParaphraseRequest(BaseModel):
    text: str

class GrammarRequest(BaseModel):
    text: str

class DetectRequest(BaseModel):
    text: str

@router.post("/seo-article")
async def seo_article(req: GenerateRequest):
    try:
        out = generate_seo_article(req.title, req.keywords, req.length)
        return {"success": True, "article": out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/paraphrase")
async def paraphrase(req: ParaphraseRequest):
    return {"success": True, "paraphrase": paraphrase_text(req.text)}

@router.post("/grammar-check")
async def grammar(req: GrammarRequest):
    return {"success": True, "corrections": grammar_check(req.text)}

@router.post("/ai-detect")
async def detect(req: DetectRequest):
    return {"success": True, "ai_probability": ai_detect(req.text)}

@router.post("/humanize")
async def humanize(req: ParaphraseRequest):
    return {"success": True, "humanized": humanize_text(req.text)}
