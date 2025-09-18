# routers/design_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.design_service import generate_image_from_prompt, create_canva_template_stub

router = APIRouter()

class ImageReq(BaseModel):
    prompt: str
    size: str = "1024x1024"

@router.post("/image-gen")
def image_gen(req: ImageReq):
    try:
        url = generate_image_from_prompt(req.prompt, req.size)
        return {"success": True, "image_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/canva-template")
def canva_template():
    return {"success": True, "msg": create_canva_template_stub()}
