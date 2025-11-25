import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PALETTE = {
    "primary": "#09728B",
    "primary_dark": "#066F91",
    "accent": "#0BA6C5",
    "muted": "#5A6A73",
    "soft": "#E6F3F7",
    "warning": "#B47515",
}

COLORWAY = [PALETTE["primary"], PALETTE["accent"], "#0A4D64", "#7C3F87", "#4A4A4A"]


def _apply_layout_defaults(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=title,
        template="plotly_white",
        colorway=COLORWAY,
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(bgcolor="white"),
        plot_bgcolor="#f9fbfd",
        paper_bgcolor="#f9fbfd",
        xaxis=dict(showgrid=False, zeroline=False, linecolor="#d8e3ea", title_font=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor="#dfe9ef", zeroline=False, title_font=dict(size=12)),
        font=dict(color=PALETTE["primary_dark"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, x=0, font=dict(size=11)),
    )
    return fig


def make_overview_kpi_cards(adoption_index: float, coverage_rate: float, avg_completion: float, total_attendance: int):
    return [
        {"label": "AI Adoption Index", "value": f"{adoption_index:.1f}", "help": "Composite indicator of readiness, adoption, and training coverage across selected departments."},
        {"label": "Training Coverage", "value": f"{coverage_rate*100:.0f}%", "help": "Share of the selected departments reached by AIRE training activities."},
        {"label": "Avg Completion", "value": f"{avg_completion*100:.0f}%", "help": "Average completion across formats for the selected time window and audiences."},
        {"label": "Total Attendances", "value": f"{total_attendance:,}", "help": "Aggregate attendances in the selected window to gauge demand and capacity needs."},
    ]


def make_adoption_radar_chart(dept_adoption_df: pd.DataFrame):
    if dept_adoption_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available for the current filters.", showarrow=False)
        return _apply_layout_defaults(fig, "AI Adoption Index by Department")
    fig = px.line_polar(dept_adoption_df, r="adoption_index", theta="department_name", line_close=True, color_discrete_sequence=[PALETTE["primary"]])
    fig.update_traces(fill="toself", hovertemplate="%{theta}<br>Adoption Index: %{r:.1f}<extra></extra>")
    return _apply_layout_defaults(fig, "Composite Readiness Profile (Adoption × Coverage × Uptake)")


def make_confidence_change_chart(impact_df: pd.DataFrame):
    if impact_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No confidence survey data available for the current filters.", showarrow=False)
        return _apply_layout_defaults(fig, "Confidence Change (Pre vs Post)")
    melted = impact_df.melt(id_vars=["metric"], value_vars=["pre_mean", "post_mean"], var_name="stage", value_name="score")
    fig = px.bar(melted, x="metric", y="score", color="stage", barmode="group", color_discrete_sequence=[PALETTE["primary"], PALETTE["accent"]])
    fig.update_layout(yaxis_title="Average Score (1-5)")
    fig.update_traces(hovertemplate="%{x} | %{legendgroup}: %{y:.2f}", marker_line_color="#ffffff", marker_line_width=0.5)
    return _apply_layout_defaults(fig, "Competency Shift Analysis: Pre- vs. Post-Intervention")


def make_workshop_engagement_timeseries(engagement_df: pd.DataFrame):
    if engagement_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No workshop activity available for the current filters.", showarrow=False)
        return _apply_layout_defaults(fig, "Attendance Over Time")
    fig = px.line(engagement_df, x="month", y="attendances", markers=True, color_discrete_sequence=[PALETTE["primary"]])
    fig.update_traces(hovertemplate="%{x|%b %Y}: %{y} attendances")
    fig.update_layout(xaxis_title="Month", yaxis_title="Attendances")
    return _apply_layout_defaults(fig, "Participation Velocity & Demand Forecasting")


def make_reflection_sentiment_bar(sentiment_df: pd.DataFrame):
    if sentiment_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No reflections available for the current filters.", showarrow=False)
        return _apply_layout_defaults(fig, "Reflection Sentiment")
    fig = px.bar(sentiment_df, x="sentiment", y="count", color="sentiment", color_discrete_map={"positive": PALETTE["primary"], "neutral": PALETTE["muted"], "negative": PALETTE["warning"]})
    fig.update_layout(xaxis_title="Sentiment", yaxis_title="Count")
    fig.update_traces(hovertemplate="%{x}: %{y}", marker_line_color="#ffffff", marker_line_width=0.5)
    return _apply_layout_defaults(fig, "Qualitative Signal: Sentiment Distribution")


def make_theme_distribution_bar(theme_df: pd.DataFrame):
    if theme_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No reflection themes available for the current filters.", showarrow=False)
        return _apply_layout_defaults(fig, "Reflection Themes")
    fig = px.bar(theme_df, x="theme", y="count", color_discrete_sequence=[PALETTE["primary"]])
    fig.update_layout(xaxis_title="Theme", yaxis_title="Count")
    fig.update_traces(hovertemplate="%{x}: %{y}", marker_line_color="#ffffff", marker_line_width=0.5)
    return _apply_layout_defaults(fig, "Thematic Analysis: Emerging Risks & Opportunities")


def make_department_readiness_scatter(readiness_df: pd.DataFrame):
    if readiness_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No readiness data available for the current filters.", showarrow=False)
        return _apply_layout_defaults(fig, "Department Readiness vs Coverage")
    fig = px.scatter(
        readiness_df,
        x="training_coverage_rate",
        y="current_readiness_score",
        size="participant_count",
        text="department_name",
        title="Readiness vs Coverage (with participant scale)",
        labels={"training_coverage_rate": "Training Coverage", "current_readiness_score": "Current Readiness"},
        color_discrete_sequence=[PALETTE["primary"]],
    )
    fig.update_traces(textposition="top center", hovertemplate="%{text}<br>Coverage: %{x:.0%}<br>Readiness: %{y:.0%}<br>Participants: %{marker.size}")
    fig.update_layout(xaxis_tickformat=".0%", yaxis_tickformat=".0%")
    fig.add_hline(y=0.7, line_dash="dot", line_color=PALETTE["muted"], annotation_text="Readiness target 70%", annotation_position="top left")
    fig.add_vline(x=0.7, line_dash="dot", line_color=PALETTE["muted"], annotation_text="Coverage target 70%", annotation_position="bottom right")
    return _apply_layout_defaults(fig, "Department Readiness vs Coverage")
