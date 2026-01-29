from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import io

def export_dashboard_pdf(dashboard_data, filename="BrandNBloom_Report.pdf"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    styleH = styles["Heading1"]
    styleN = styles["Normal"]

    elements.append(Paragraph("🌸 Brand N Bloom - Combined Analytics Report", styleH))
    elements.append(Spacer(1, 20))

    # Summary KPIs
    elements.append(Paragraph("📌 Summary KPIs", styles["Heading2"]))
    kpi_data = []

    churn_df = dashboard_data.get("Churn Predictor", pd.DataFrame())
    clv_df = dashboard_data.get("CLV Calculator", pd.DataFrame())
    roi_df = dashboard_data.get("ROI Tracker", pd.DataFrame())
    ads_df = dashboard_data.get("Ad Creative Tester", pd.DataFrame())

    kpi_data.append(["Total Customers", len(churn_df)])
    kpi_data.append(["Avg CLV", round(clv_df["CLV"].mean(), 2) if not clv_df.empty else 0])
    kpi_data.append(["Predicted Churn %", round(churn_df["ChurnPrediction"].mean()*100,2) if "ChurnPrediction" in churn_df else 0])
    kpi_data.append(["Total ROI %", round(roi_df["ROI"].sum(),2) if "ROI" in roi_df else 0])
    kpi_data.append(["Top CTR %", round(ads_df["CTR"].max(),2) if "CTR" in ads_df else 0])

    table = Table(kpi_data)
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Tool-wise details
    for tool_name, df in dashboard_data.items():
        elements.append(Paragraph(f"📌 {tool_name}", styles["Heading2"]))
        # Show top 10 rows
        if not df.empty:
            table_data = [df.columns.tolist()] + df.head(10).values.tolist()
            elements.append(Table(table_data))
        # AI captions
        if "AI_Insight" in df.columns:
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"💡 AI Insight: {df['AI_Insight'].iloc[0]}", styleN))
        elements.append(Spacer(1, 15))

    doc.build(elements)
    buffer.seek(0)
    return buffer
