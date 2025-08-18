import os, requests, json

MAILERLITE_API_KEY = os.environ.get("MAILERLITE_API_KEY")
MAILERLITE_BASE = "https://api.mailerlite.com/api/v2"

def send_campaign(subject: str, html: str, group_id: str = None):
    if not MAILERLITE_API_KEY:
        raise RuntimeError("MAILERLITE_API_KEY missing in env")
    headers = {"Content-Type":"application/json", "X-MailerLite-ApiKey": MAILERLITE_API_KEY}
    # This is a simplified example: create campaign and send to group.
    payload = {"subject": subject, "type": "regular", "groups": [group_id] if group_id else [] , "html": html}
    # In real usage, use proper MailerLite endpoints and follow API steps (create campaign -> send)
    resp = requests.post(MAILERLITE_BASE + "/campaigns", headers=headers, data=json.dumps(payload))
    return resp.status_code, resp.text
