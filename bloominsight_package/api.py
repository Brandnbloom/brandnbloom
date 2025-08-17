from flask import Flask, request, jsonify
from instagram_client import InstagramClient
from db import Database
from analytics import analyze_posts, compute_brand_health
import os

app = Flask(__name__)
db = Database(os.environ.get("DATABASE_PATH", "data/bloominsight.db"))
client = InstagramClient()

@app.route("/scrape/profile", methods=["POST"])
def scrape_profile():
    data = request.json or {}
    username = data.get("username")
    if not username:
        return jsonify({"error":"username required"}), 400
    profile, posts = client.fetch_profile_and_posts(username, limit=data.get("limit", 20))
    # store raw fetch
    db.insert_profile_snapshot(username, profile, posts)
    # run analysis
    kpis = analyze_posts(profile, posts)
    health = compute_brand_health(profile, posts)
    result = {"profile":profile, "kpis":kpis, "brand_health":health}
    return jsonify(result)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok","service":"BloomInsight API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
