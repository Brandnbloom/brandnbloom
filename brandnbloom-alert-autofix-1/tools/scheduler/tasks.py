from apscheduler.schedulers.blocking import BlockingScheduler
import os, requests
from reports.report_generator import create_weekly_pdf
import smtplib
from email.message import EmailMessage
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL

sched = BlockingScheduler(timezone='UTC')

def daily_pull(handle):
    url = os.environ.get('BACKEND_SCRAPE_URL','http://localhost:8000/scrape')
    r = requests.post(url, json={'handle':handle,'limit':25}, timeout=120)
    print('Pull', r.status_code, r.text)

def send_weekly(handle, recipient):
    pdf = create_weekly_pdf(handle)
    msg = EmailMessage()
    msg['Subject'] = f'BloomInsight Weekly - {handle}'
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient
    msg.set_content('Weekly report attached.')
    with open(pdf,'rb') as f:
        data = f.read()
        msg.add_attachment(data, maintype='application', subtype='pdf', filename=os.path.basename(pdf))
    s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    s.starttls()
    s.login(SMTP_USER, SMTP_PASS)
    s.send_message(msg)
    s.quit()

if __name__ == '__main__':
    handles = ['natgeo']
    for h in handles:
        sched.add_job(daily_pull, 'cron', args=[h], hour=int(os.environ.get('DAILY_PULL_CRON_HOUR_UTC',2)))
    sched.add_job(send_weekly, 'cron', day_of_week='mon', hour=int(os.environ.get('DAILY_PULL_CRON_HOUR_UTC',3)), args=['natgeo','client@example.com'])
    sched.start()
