from __future__ import annotations
from typing import List, Tuple, Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
import os


def build_pdf(path: str,
              title: str,
              kpis: List[Tuple[str, str]],
              charts: List[str],
              insights: Dict[str, Any]) -> str:
    doc = SimpleDocTemplate(path, pagesize=A4, title=title)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{title}</b>", styles['Title']))
    story.append(Spacer(1, 12))

    # KPIs table
    data = [["Metric", "Value"]] + [[k, v] for k, v in kpis]
    tbl = Table(data, hAlign='LEFT')
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f2f2f2')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 16))

    # Charts images
    for chart_path in charts:
        if os.path.exists(chart_path):
            story.append(Image(chart_path, width=6.5*inch, height=3.2*inch))
            story.append(Spacer(1, 8))

    # Insights / Recommendations
    story.append(Paragraph("<b>Analysis & Recommendations</b>", styles['Heading2']))

    
