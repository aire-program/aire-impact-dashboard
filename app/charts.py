import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT

def plot_registrations_vs_attendance(workshops_df: pd.DataFrame):
    """Bar chart of registrations vs attendance over time."""
    df = workshops_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["date"], y=df["registrations"], name="Registrations", marker_color=COLOR_SECONDARY))
    fig.add_trace(go.Bar(x=df["date"], y=df["attended"], name="Attended", marker_color=COLOR_PRIMARY))
    
    fig.update_layout(
        title="Registrations vs Attendance Over Time",
        xaxis_title="Date",
        yaxis_title="Count",
        barmode="group",
        template="plotly_white"
    )
    return fig

def plot_readiness_distribution(assessments_post_df: pd.DataFrame):
    """Histogram of overall readiness scores."""
    fig = px.histogram(
        assessments_post_df, 
        x="overall_readiness", 
        nbins=5, 
        title="Distribution of Post-Workshop Readiness Scores",
        color_discrete_sequence=[COLOR_PRIMARY]
    )
    fig.update_layout(template="plotly_white", xaxis_title="Readiness Score (1-5)", yaxis_title="Count")
    return fig

def plot_sentiment_breakdown(reflections_df: pd.DataFrame):
    """Pie chart of sentiment."""
    counts = reflections_df["sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]
    
    fig = px.pie(
        counts, 
        values="count", 
        names="sentiment", 
        title="Reflection Sentiment Breakdown",
        color_discrete_sequence=[COLOR_PRIMARY, COLOR_ACCENT, "#E63946"]
    )
    return fig

def plot_adoption_trends(adoption_events_df: pd.DataFrame):
    """Line chart of adoption events over time."""
    df = adoption_events_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    monthly = df.resample("M", on="date").size().reset_index(name="count")
    
    fig = px.line(
        monthly, 
        x="date", 
        y="count", 
        title="Adoption Events Over Time (Monthly)",
        markers=True,
        color_discrete_sequence=[COLOR_PRIMARY]
    )
    fig.update_layout(template="plotly_white")
    return fig
