# brandnbloom/api.py

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from brandnbloom.bloomscore_pro_v2 import generate_full_report
from PIL import Image
import io
import json
import logging

# ----------------------------------------------------
# App Initialization
# ----------------------------------------------------
app = FastAPI(title="BloomScore Pro v2 API", version="2.0")

# ----------------------------------------------------
# CORS (Allow dashboard to call API from Streamlit)
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Logger
# ----------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bloom_api")


# ----------------------------------------------------
# Utility: Validate uploaded image
# ----------------------------------------------------
def validate_image(contents: bytes):
    try:
        Image.open(io.BytesIO(contents))
        return True
    except Exception:
        return False


# ----------------------------------------------------
# API Endpoint
# ----------------------------------------------------
@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    sample_texts: str = Form(None),
    competitors: str = Form(None),
    industry: str = Form("default"),
    account_type: str = Form("personal_brand")
):
    """
    Upload a screenshot image + optional text.
    Returns HTML preview + PDF export path.
    """

    # ------------------------------
    # 1) Validate: File extension
    # ------------------------------
    allowed_ext = ["jpg", "jpeg", "png", "webp"]

    if not file.filename.lower().split(".")[-1] in allowed_ext:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image type. Allowed: {allowed_ext}"
        )

    # ------------------------------
    # 2) Read file
    # ------------------------------
    img_bytes = await file.read()

    if not validate_image(img_bytes):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image."
        )

    # ------------------------------
    # 3) Parse sample_texts (JSON safe)
    # ------------------------------
    texts = []
    if sample_texts:
        try:
            texts = json.loads(sample_texts)
            if not isinstance(texts, list):
                texts = [str(texts)]
        except json.JSONDecodeError:
            texts = [sample_texts]  # fallback

    # ------------------------------
    # 4) Parse competitors
    # ------------------------------
    comps = []
    if competitors:
        try:
            comps = [float(x.strip()) for x in competitors.split(",") if x.strip()]
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Competitors must be numbers separated by commas."
            )

    # ------------------------------
    # Report Data Structure
    # ------------------------------
    profile = {
        "image_bytes": img_bytes,
        "sample_texts": texts,
        "metrics": {},
        "brand_palette": None,
    }

    try:
        logger.info("Generating brand report...")
        report = generate_full_report(
            profile,
            competitors=comps,
            industry=industry,
            account_type=account_type
        )
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail="Error generating report.")

    # ------------------------------
    # Final Response
    # ------------------------------
    return JSONResponse(
        {
            "status": "success",
            "html_preview": report.get("html"),
            "pdf_path": report.get("pdf_path"),
            "meta": {
                "texts_used": len(texts),
                "competitors_used": len(comps),
                "industry": industry,
                "account_type": account_type
            }
        }
    )
