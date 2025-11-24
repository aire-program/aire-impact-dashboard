import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def make_overview_kpi_cards(adoption_index: float, coverage_rate: float, avg_completion: float, total_attendance: int):
    return [
        {"label": "AI Adoption Index", "value": f"{adoption_index:.1f}", "help": "Composite of readiness, adoption, and coverage."},
        {"label": "Training Coverage", "value": f"{coverage_rate*100:.0f}%", "help": "Share of each department trained."},
        {"label": "Avg Completion", "value": f"{avg_completion*100:.0f}%", "help": "Completion rate across learning formats."},
        {"label": "Total Attendances", "value": f"{total_attendance:,}", "help": "Sum of attendances in the selected range."},
    ]


def make_adoption_radar_chart(dept_adoption_df: pd.DataFrame):
    if dept_adoption_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data for this selection", showarrow=False)
        return fig
    fig = px.line_polar(dept_adoption_df, r="adoption_index", theta="department_name", line_close=True)
    fig.update_traces(fill="toself")
    fig.update_layout(title="AI Adoption Index by Department", showlegend=False)
    return fig


def make_confidence_change_chart(impact_df: pd.DataFrame):
    if impact_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No confidence survey data for this selection", showarrow=False)
        return fig
    melted = impact_df.melt(id_vars=["metric"], value_vars=["pre_mean", "post_mean"], var_name="stage", value_name="score")
    fig = px.bar(melted, x="metric", y="score", color="stage", barmode="group", title="Confidence Change (Pre vs Post)")
    fig.update_layout(yaxis_title="Average Score (1-5)")
    return fig


def make_workshop_engagement_timeseries(engagement_df: pd.DataFrame):
    if engagement_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No workshop activity for this selection", showarrow=False)
        return fig
    fig = px.line(engagement_df, x="month", y="attendances", markers=True, title="Attendance Over Time")
    fig.update_layout(xaxis_title="Month", yaxis_title="Attendances")
    return fig


def make_reflection_sentiment_bar(sentiment_df: pd.DataFrame):
    if sentiment_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No reflections for this selection", showarrow=False)
        return fig
    fig = px.bar(sentiment_df, x="sentiment", y="count", title="Reflection Sentiment")
    fig.update_layout(xaxis_title="Sentiment", yaxis_title="Count")
    return fig


def make_theme_distribution_bar(theme_df: pd.DataFrame):
    if theme_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No reflection themes for this selection", showarrow=False)
        return fig
    fig = px.bar(theme_df, x="theme", y="count", title="Reflection Themes")
    fig.update_layout(xaxis_title="Theme", yaxis_title="Count")
    return fig


def make_department_readiness_scatter(readiness_df: pd.DataFrame):
    if readiness_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No readiness data for this selection", showarrow=False)
        return fig
    fig = px.scatter(
        readiness_df,
        x="training_coverage_rate",
        y="current_readiness_score",
        size="participant_count",
        text="department_name",
        title="Department Readiness vs Coverage",
        labels={"training_coverage_rate": "Training Coverage", "current_readiness_score": "Current Readiness"},
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(xaxis_tickformat=".0%", yaxis_tickformat=".0%")
    return fig
