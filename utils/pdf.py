from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def make_report(pdf_path: str, title: str, kpis: dict, action_plan: list[str], logo_path: str = None):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    if logo_path:
        try:
            from reportlab.platypus import Image
            c.drawImage(logo_path, width-6*cm, height-3*cm, width=4*cm, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    c.drawString(2*cm, height-2*cm, title)

    c.setFont("Helvetica", 11)
    c.drawString(2*cm, height-3.2*cm, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    y = height - 4.2*cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2*cm, y, "KPIs")
    y -= 0.8*cm
    c.setFont("Helvetica", 11)
    for k, v in kpis.items():
        c.drawString(2.2*cm, y, f"- {k}: {v}")
        y -= 0.6*cm

    y -= 0.4*cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2*cm, y, "Action Plan")
    y -= 0.8*cm
    c.setFont("Helvetica", 11)
    for step in action_plan:
        c.drawString(2.2*cm, y, f"- {step}")
        y -= 0.6*cm
        if y < 2*cm:
            c.showPage()
            y = height - 2*cm
    c.showPage()
    c.save()
    return pdf_path
