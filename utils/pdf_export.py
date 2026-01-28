from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

def generate_pdf_report(user_id, dashboard_data):
    """
    dashboard_data = list of dicts:
    [
        {
          'tool': 'Customer 360 + RFM',
          'kpis': {'CLV': 12000, 'Churn Risk': 'High'},
          'ai_summary': 'AI-generated insights...',
          'chart_paths': ['charts/rfm.png']
        }
    ]
    """

    os.makedirs("exports", exist_ok=True)

    file_name = f"exports/Brand_N_Bloom_Report_{user_id}.pdf"

    pdf = SimpleDocTemplate(file_name, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # ---- Title ----
    elements.append(Paragraph(
        "<b>Brand N Bloom — Growth Intelligence Report</b>",
        styles["Title"]
    ))
    elements.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %b %Y')}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    # ---- Loop through tools ----
    for block in dashboard_data:
        elements.append(Paragraph(
            f"<b>{block['tool']}</b>",
            styles["Heading2"]
        ))
        elements.append(Spacer(1, 10))

        # KPIs
        for k, v in block["kpis"].items():
            elements.append(Paragraph(
                f"{k}: <b>{v}</b>",
                styles["Normal"]
            ))

        elements.append(Spacer(1, 10))

        # AI summary
        elements.append(Paragraph(
            block["ai_summary"],
            styles["Italic"]
        ))
        elements.append(Spacer(1, 15))

        # Charts
        for chart in block["chart_paths"]:
            if os.path.exists(chart):
                elements.append(Image(chart, width=400, height=250))
                elements.append(Spacer(1, 20))

        elements.append(PageBreak())

    pdf.build(elements)
    return file_name
