# brandnbloom/api.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from brandnbloom.bloomscore_pro_v2 import generate_full_report
import base64

app = FastAPI(title="BloomScore Pro v2 API")


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), sample_texts: str = Form(None), competitors: str = Form(None), industry: str = Form("default"), account_type: str = Form("personal_brand")):
    """
    Upload a screenshot image and optional texts (JSON list string).
    Returns HTML and path to PDF (if exported).
    """
    img_bytes = await file.read()
    texts = []
    try:
        import json
        if sample_texts:
            texts = json.loads(sample_texts)
    except Exception:
        texts = [sample_texts] if sample_texts else []

    comps = []
    try:
        if competitors:
            comps = [float(x) for x in competitors.split(",") if x.strip()]
    except Exception:
        comps = []

    profile = {
        "image_bytes": img_bytes,
        "sample_texts": texts,
        "metrics": {},          # API caller can extend
        "brand_palette": None
    }

    report = generate_full_report(profile, competitors=comps, industry=industry, account_type=account_type)
    return JSONResponse({"html_preview": report["html"], "pdf_path": report["pdf_path"]})
