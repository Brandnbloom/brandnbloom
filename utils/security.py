# utils/pdf.py

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm


def make_report(
    pdf_path: str,
    title: str,
    kpis: dict,
    action_plan: list[str],
    logo_path: str = None
):
    """
    Generates a clean business-style PDF report using Platypus.
    """
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    story = []

    # ---------------------------------------------------------
    # Logo
    # ---------------------------------------------------------
    if logo_path:
        try:
            img = Image(logo_path, width=4 * cm, preserveAspectRatio=True, mask="auto")
            img.hAlign = "RIGHT"
            story.append(img)
        except Exception:
            pass

    # ---------------------------------------------------------
    # Title
    # ---------------------------------------------------------
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=20,
        spaceAfter=12,
    )
    story.append(Paragraph(title, title_style))

    # Timestamp
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    story.append(Paragraph(f"<i>Generated on: {ts}</i>", styles["Normal"]))
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # KPI Table
    # ---------------------------------------------------------
    story.append(Paragraph("<b>Key Performance Indicators</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    table_data = [["Metric", "Value"]]
    for k, v in kpis.items():
        table_data.append([k, str(v)])

    kpi_table = Table(table_data, colWidths=[8 * cm, 6 * cm])
    kpi_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONT", (0, 1), (-1, -1), "Helvetica"),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ])
    )
    story.append(kpi_table)
    story.append(Spacer(1, 20))

    # ---------------------------------------------------------
    # Action Plan (bulleted)
    # ---------------------------------------------------------
    story.append(Paragraph("<b>Action Plan</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    for step in action_plan:
        story.append(Paragraph(f"• {step}", styles["Normal"]))
        story.append(Spacer(1, 6))

    # ---------------------------------------------------------
    # Build PDF
    # ---------------------------------------------------------
    doc.build(story)
    return pdf_path
