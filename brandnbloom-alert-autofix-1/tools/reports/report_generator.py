from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from backend.db import SessionLocal, Account, Post
import matplotlib.pyplot as plt, io
from datetime import datetime

def create_weekly_pdf(handle, out_path=None):
    db = SessionLocal()
    acc = db.query(Account).filter(Account.handle==handle).first()
    if not acc:
        raise ValueError('No data for handle')
    posts = db.query(Post).filter(Post.account_id==acc.id).order_by(Post.timestamp.desc()).limit(30).all()
    if out_path is None:
        os.makedirs('reports', exist_ok=True)
        out_path = f'reports/{handle}_weekly_{datetime.utcnow().strftime("%Y%m%d")}.pdf'
    times = [p.timestamp for p in posts if p.timestamp]
    likes = [p.like_count or 0 for p in posts if p.timestamp]
    buf = None
    if times and likes:
        plt.figure(figsize=(6,3))
        plt.plot(times[::-1], likes[::-1])
        plt.tight_layout()
        b = io.BytesIO()
        plt.savefig(b, format='png')
        b.seek(0)
        buf = b
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-60, f'BloomInsight Weekly — {handle}')
    c.setFont('Helvetica', 10)
    c.drawString(40, height-90, f'Followers: {acc.followers or 0}')
    if buf:
        c.drawImage(buf, 40, height-300, width=500, preserveAspectRatio=True)
    c.showPage()
    c.save()
    return out_path
