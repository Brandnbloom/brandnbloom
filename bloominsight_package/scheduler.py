from apscheduler.schedulers.background import BackgroundScheduler
import os
from api import scrape_profile
from report_generator import create_weekly_pdf
from db import Database
import smtplib
from email.message import EmailMessage

def daily_pull(username):
    # hit the local api to scrape (or directly call client)
    import requests
    url = f"http://localhost:8000/scrape/profile"
    r = requests.post(url, json={"username":username,"limit":20})
    return r.json()

def send_weekly_report(username, recipient):
    pdf = create_weekly_pdf(username)
    # send via SMTP
    import smtplib
    from email.message import EmailMessage
    cfg = __import__('config')
    msg = EmailMessage()
    msg['Subject'] = f"BloomInsight Weekly Report - {username}"
    msg['From'] = cfg.FROM_EMAIL
    msg['To'] = recipient
    msg.set_content("Attached weekly report.")
    with open(pdf,'rb') as f:
        data = f.read()
        msg.add_attachment(data, maintype='application', subtype='pdf', filename=os.path.basename(pdf))
    s = smtplib.SMTP(cfg.SMTP_HOST, cfg.SMTP_PORT)
    s.starttls()
    s.login(cfg.SMTP_USER, cfg.SMTP_PASS)
    s.send_message(msg)
    s.quit()

def start_scheduler(username, recipient):
    sched = BackgroundScheduler(timezone='UTC')
    # schedule daily pull at configured hour
    cfg = __import__('config')
    sched.add_job(daily_pull, 'cron', hour=cfg.DAILY_PULL_HOUR_UTC, args=[username])
    # schedule weekly report
    sched.add_job(send_weekly_report, 'cron', day_of_week='mon', hour=cfg.DAILY_PULL_HOUR_UTC+1, args=[username, recipient])
    sched.start()
    return sched
