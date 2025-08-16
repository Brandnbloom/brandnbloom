from flask import Flask, request, redirect, jsonify
import requests, os

app = Flask(__name__)

FB_APP_ID = os.environ['FB_APP_ID']
FB_APP_SECRET = os.environ['FB_APP_SECRET']
REDIRECT_URI = "https://your-api-url.onrender.com/callback"

@app.route("/connect")
def connect():
    scopes = "instagram_basic,instagram_manage_insights,pages_read_engagement"
    return redirect(f"https://www.facebook.com/v17.0/dialog/oauth?client_id={FB_APP_ID}&redirect_uri={REDIRECT_URI}&scope={scopes}")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://graph.facebook.com/v17.0/oauth/access_token"
    params = {
        "client_id": FB_APP_ID,
        "client_secret": FB_APP_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    r = requests.get(token_url, params=params).json()
    return jsonify(r)  # send token to your dashboard or save in DB

@app.route("/insights")
def insights():
    access_token = request.args.get("token")
    ig_user_id = request.args.get("ig_user_id")
    metrics = "impressions,reach,profile_views"
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/insights"
    params = {"metric": metrics, "period": "day", "access_token": access_token}
    r = requests.get(url, params=params).json()
    return jsonify(r)
