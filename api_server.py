from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging, threading

# --------- IMPORTS ---------
from bloominsight.scraper import fetch_public_profile
from bloominsight.analyzer import analyze_profile
from ai_tools.bloomscore import compute_bloomscore
from ai_tools.influencer_finder import find_influencers
from ai_tools.business_compare import compare_handles
from ai_tools.menu_pricing import suggest_prices
from ai_tools.consumer_behavior import run_questionnaire
from bloominsight.report_api import generate_and_send_weekly_report
from db.models import log_kpis, save_report
from utils_sitemap import update_sitemap_and_ping
from auth.users import create_user, verify_user  # assuming you have this

# --------- SETUP ---------
logger = logging.getLogger("uvicorn.error")
app = FastAPI(title="Brand N Bloom API")

# Run sitemap updater in background (non-blocking)
threading.Thread(target=update_sitemap_and_ping, daemon=True).start()

# --------- GLOBAL ERROR HANDLERS ---------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url}: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# --------- MODELS ---------
class HandleRequest(BaseModel):
    handle: str

class ReportRequest(BaseModel):
    handle: str
    email: str
    user_id: Optional[int] = 1

class CompareRequest(BaseModel):
    handles: List[str]

class MenuSuggestRequest(BaseModel):
    cost: float
    margin: Optional[float] = 40
    competitor: Optional[float] = None

class ConsumerRequest(BaseModel):
    answers: Dict

class SignupRequest(BaseModel):
    email: str
    name: Optional[str] = None
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# --------- ROUTES ---------
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/scrape")
def scrape(req: HandleRequest):
    try:
        return fetch_public_profile(req.handle)
    except Exception as e:
        logger.error(f"/scrape failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile")

@app.post("/analyze")
def analyze(req: HandleRequest):
    try:
        profile = fetch_public_profile(req.handle)
        analysis = analyze_profile(profile)
        try:
            log_kpis(req.handle, analysis['followers'], analysis['likes'], analysis['reach'],
                     analysis['impressions'], analysis['engagement_rate'])
        except Exception as e:
            logger.warning(f"DB log error for {req.handle}: {e}")
        return analysis
    except Exception as e:
        logger.error(f"/analyze failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze profile")

@app.post("/send-report")
def send_report(req: ReportRequest):
    try:
        profile = fetch_public_profile(req.handle)
        analysis = analyze_profile(profile)
        kpis = {
            "Followers": analysis["followers"],
            "Likes": analysis["likes"],
            "Reach": analysis["reach"],
            "Impressions": analysis["impressions"],
            "Engagement Rate (%)": analysis["engagement_rate"],
        }
        pdf = generate_and_send_weekly_report(req.user_id, req.email, req.handle, kpis)
        return {"status": "sent", "pdf": pdf}
    except Exception as e:
        logger.error(f"/send-report failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to send report")

@app.post("/bloomscore")
def bloomscore_api(req: HandleRequest):
    try:
        p = fetch_public_profile(req.handle)
        return compute_bloomscore(p)
    except Exception as e:
        logger.error(f"/bloomscore failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to compute bloomscore")

@app.post("/influencers")
def influencers_api(req: CompareRequest):
    try:
        return find_influencers(req.handles)
    except Exception as e:
        logger.error(f"/influencers failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to find influencers")

@app.post("/menu-suggest")
def menu_suggest_api(req: MenuSuggestRequest):
    try:
        return suggest_prices(req.cost, req.margin, req.competitor)
    except Exception as e:
        logger.error(f"/menu-suggest failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to suggest prices")

@app.post("/consumer")
def consumer_api(req: ConsumerRequest):
    try:
        return run_questionnaire(req.answers)
    except Exception as e:
        logger.error(f"/consumer failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to run questionnaire")

@app.post("/compare")
def compare(req: CompareRequest):
    results = {}
    for h in req.handles:
        try:
            p = fetch_public_profile(h)
            a = analyze_profile(p)
            results[h] = {"followers": a["followers"], "engagement_rate": a["engagement_rate"]}
        except Exception:
            results[h] = {"error": "Failed to analyze handle"}
    return results

@app.post("/signup")
def signup(req: SignupRequest):
    try:
        user_id = create_user(req.email, req.name, req.password)
        return {"status": "ok", "user_id": user_id}
    except Exception as e:
        logger.error(f"/signup failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to create user")

@app.post("/login")
def login(req: LoginRequest):
    try:
        if verify_user(req.email, req.password):
            return {"status": "ok"}
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"/login failed: {e}")
        raise HTTPException(status_code=500, detail="Login failed")
