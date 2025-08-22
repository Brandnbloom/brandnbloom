from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
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

# Run sitemap updater in background (non-blocking)
import threading
threading.Thread(target=update_sitemap_and_ping, daemon=True).start()

app = FastAPI(title="Brand N Bloom API")

# ---------- MODELS ----------
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

# ---------- ROUTES ----------
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/scrape")
def scrape(req: HandleRequest):
    return fetch_public_profile(req.handle)

@app.post("/analyze")
def analyze(req: HandleRequest):
    profile = fetch_public_profile(req.handle)
    analysis = analyze_profile(profile)
    try:
        log_kpis(req.handle, analysis['followers'], analysis['likes'], analysis['reach'], analysis['impressions'], analysis['engagement_rate'])
    except Exception as e:
        print("DB log error:", e)
    return analysis

@app.post("/send-report")
def send_report(req: ReportRequest):
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

@app.post("/bloomscore")
def bloomscore_api(req: HandleRequest):
    p = fetch_public_profile(req.handle)
    return compute_bloomscore(p)

@app.post("/influencers")
def influencers_api(req: CompareRequest):
    return find_influencers(req.handles)

@app.post("/menu-suggest")
def menu_suggest_api(req: MenuSuggestRequest):
    return suggest_prices(req.cost, req.margin, req.competitor)

@app.post("/consumer")
def consumer_api(req: ConsumerRequest):
    return run_questionnaire(req.answers)

@app.post("/compare")
def compare(req: CompareRequest):
    results = {}
    for h in req.handles:
        try:
            p = fetch_public_profile(h)
            a = analyze_profile(p)
            results[h] = {"followers": a["followers"], "engagement_rate": a["engagement_rate"]}
        except Exception as e:
            results[h] = {"error": str(e)}
    return results

@app.post("/signup")
def signup(req: SignupRequest):
    user_id = create_user(req.email, req.name, req.password)
    return {"status": "ok", "user_id": user_id}

@app.post("/login")
def login(req: LoginRequest):
    if verify_user(req.email, req.password):
        return {"status": "ok"}
    return {"error": "invalid credentials"}
