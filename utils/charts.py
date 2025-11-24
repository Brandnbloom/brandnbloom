import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def kpi_line(
    df: pd.DataFrame,
    y: str,
    title: str,
    rolling_window: int | None = None,
    comparison_df: pd.DataFrame | None = None,
    comparison_label: str = "Comparison",
    show_markers: bool = True,
    dark_mode: bool = False,
):
    """
    Enhanced KPI Line Chart with optional rolling average, comparison line,
    markers, and dark/light theme.

    Args:
        df: Main DataFrame with time-series KPI data.
        y: Column name to plot.
        title: Chart title.
        rolling_window: e.g., 7, 14 -> shows rolling average on chart.
        comparison_df: Optional second dataframe for comparison.
        comparison_label: Label for comparison line.
        show_markers: Show dots on data points.
        dark_mode: Enables dark theme.

    Returns:
        Plotly Figure or None if df is empty.
    """

    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18)
        )
        fig.update_layout(title=title, margin=dict(l=10, r=10, t=40, b=10))
        return fig

    df_sorted = df.sort_values("timestamp")

    # Base figure
    fig = go.Figure()

    # ---- MAIN LINE ----
    fig.add_trace(
        go.Scatter(
            x=df_sorted["timestamp"],
            y=df_sorted[y],
            mode="lines+markers" if show_markers else "lines",
            name=y,
            line=dict(width=2),
        )
    )

    # ---- ROLLING AVERAGE ----
    if rolling_window:
        df_sorted[f"{y}_rolling"] = df_sorted[y].rolling(rolling_window).mean()
        fig.add_trace(
            go.Scatter(
                x=df_sorted["timestamp"],
                y=df_sorted[f"{y}_rolling"],
                mode="lines",
                name=f"{rolling_window}-day Avg",
                line=dict(dash="dash", width=2),
            )
        )

    # ---- COMPARISON SERIES ----
    if comparison_df is not None and not comparison_df.empty:
        comp = comparison_df.sort_values("timestamp")
        fig.add_trace(
            go.Scatter(
                x=comp["timestamp"],
                y=comp[y],
                mode="lines",
                name=comparison_label,
                line=dict(width=2, dash="dot"),
            )
        )

    # ---- LAYOUT ----
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode="x unified",
        template="plotly_dark" if dark_mode else "plotly_white",
        legend=dict(title=""),
    )

    return fig
