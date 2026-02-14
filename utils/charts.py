import plotly.express as px
import pandas as pd

def kpi_line(df: pd.DataFrame, y: str, title: str):
    if df.empty:
        return None
    fig = px.line(df.sort_values("timestamp"), x="timestamp", y=y, title=title)
    fig.update_layout(margin=dict(l=10,r=10,t=40,b=10))
    return fig
