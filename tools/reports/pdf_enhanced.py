# Enhanced PDF report generator embedding plots and KPI table
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt, io, os
from backend.db import SessionLocal, Account, Post
from datetime import datetime
import pandas as pd

def generate_rich_pdf(handle, out_path=None):
    db = SessionLocal()
    acc = db.query(Account).filter(Account.handle==handle).first()
    if not acc:
        raise ValueError('No data for handle')
    posts = db.query(Post).filter(Post.account_id==acc.id).order_by(Post.timestamp.desc()).limit(60).all()
    if out_path is None:
        os.makedirs('reports', exist_ok=True)
        out_path = f'reports/{handle}_rich_{datetime.utcnow().strftime("%Y%m%d")}.pdf'
    # prepare dataframe
    df = pd.DataFrame([{'timestamp':p.timestamp, 'likes':p.like_count or 0, 'comments':p.comment_count or 0} for p in posts])
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        # plot likes + comments
        plt.figure(figsize=(8,3))
        plt.plot(df['timestamp'], df['likes'], label='likes')
        plt.plot(df['timestamp'], df['comments'], label='comments')
        plt.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
    else:
        buf = None
    c = canvas.Canvas(out_path, pagesize=A4)
    w,h = A4
    c.setFont('Helvetica-Bold', 18)
    c.drawString(40, h-60, f'BloomInsight Report — {handle}')
    c.setFont('Helvetica', 11)
    c.drawString(40, h-90, f'Followers: {acc.followers or 0}')
    if buf:
        img = ImageReader(buf)
        c.drawImage(img, 40, h-350, width=500, preserveAspectRatio=True)
    # KPI table
    start_y = h-370
    c.setFont('Helvetica-Bold',12)
    c.drawString(40, start_y, 'Recent Posts (most recent first)')
    c.setFont('Helvetica',10)
    y = start_y - 20
    for p in posts[:12]:
        txt = f"{p.timestamp.strftime('%Y-%m-%d %H:%M') if p.timestamp else ''}  Likes:{p.like_count or 0}  Comments:{p.comment_count or 0}"
        c.drawString(40, y, txt)
        y -= 14
        if y < 80:
            c.showPage()
            y = h-80
    c.showPage()
    c.save()
    return out_path
