# brandnbloom/report_generator.py
from typing import Dict
import tempfile
import os
from jinja2 import Template

# Optional: PDF export libs. WeasyPrint recommended.
try:
    from weasyprint import HTML
except Exception:
    HTML = None

from ai_tools.insights_to_caption import insights_to_caption

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>BloomScore Report</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Poppins', sans-serif; background:#FFF9F5; color:#3C2F2F; padding: 24px; }
    .card { background:#fff; border-radius:12px; padding:18px; box-shadow:0 6px 20px rgba(0,0,0,0.06); margin-bottom:16px; }
    .title { font-size:28px; background:linear-gradient(90deg,#A25A3C,#C28F73); -webkit-background-clip:text; color:transparent; font-weight:700; }
    .metric { font-size:34px; font-weight:700; }
    .small { color:#6b6b6b; font-size:13px; }
    .palette { display:flex; gap:8px; margin-top:8px; }
    .chip { width:44px; height:44px; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.04); }
  </style>
</head>
<body>
  <div class="card">
    <div class="title">BloomScore Pro v2 Report</div>
    <div class="small">Generated automatically</div>
  </div>

  <div class="card">
    <h3>Overall BloomScore</h3>
    <div class="metric">{{ score }}</div>
    <div class="small">Bucket: {{ bucket }}</div>
  </div>

  <div class="card">
    <h3>Component Scores</h3>
    <ul>
      {% for k,v in components.items() %}
      <li><strong>{{ k.replace('_',' ').title() }}</strong>: {{ v }}</li>
      {% endfor %}
    </ul>
  </div>

  <div class="card">
    <h3>Palette</h3>
    <div class="palette">
      {% for c in palette %}
        <div class="chip" style="background: {{ c }}"></div>
      {% endfor %}
    </div>
  </div>

  <div class="card">
    <h3>Benchmarking</h3>
    <ul>
      <li>Industry avg: {{ benchmark.industry_average }}</li>
      <li>Vs competitors (avg): {{ benchmark.avg_competitor_score }}</li>
      <li>Vs ideal: {{ benchmark.ideal_score }} ({{ benchmark.status }})</li>
    </ul>
  </div>

  {% if auto_caption %}
  <div class="card">
    <h3>Auto Caption Suggestion</h3>
    <p>{{ auto_caption }}</p>
  </div>
  {% endif %}
</body>
</html>
"""

def render_html_report(payload: Dict, generate_caption: bool = False, analysis_output: dict = None) -> str:
    """
    Returns HTML string for the report.
    payload should include: score, bucket, components (dict), palette (list), benchmark (dict)
    Optionally generates an auto caption using analysis_output.
    """
    if generate_caption and analysis_output:
        payload["auto_caption"] = insights_to_caption(analysis_output)
    else:
        payload["auto_caption"] = None

    tpl = Template(HTML_TEMPLATE)
    return tpl.render(**payload)


def export_pdf_from_html(html_str: str, out_path: str) -> str:
    """
    Export HTML to PDF using WeasyPrint (if installed).
    Returns path to PDF.
    """
    if HTML is None:
        raise RuntimeError("WeasyPrint not installed. Install weasyprint to enable PDF exports.")
    HTML(string=html_str).write_pdf(out_path)
    return out_path
