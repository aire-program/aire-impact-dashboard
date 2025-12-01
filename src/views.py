import streamlit as st
import pandas as pd
from typing import List, Optional

from src.layout_components import (
    render_adoption_section,
    render_department_focus,
    render_department_readiness_section,
    render_executive_notes,
    render_learning_impact_section,
    render_overview_section,
    render_participation_section,
    render_reflection_section,
)
from src.kpi_calculations import (
    compute_workshop_engagement,
    compute_reflection_sentiment,
)
from src.filters import filter_by_departments

def render_overview_tab(
    adoption_overall: float,
    coverage_rate: float,
    avg_completion: float,
    total_attendance: int,
    readiness_df: pd.DataFrame,
    impact_summary_df: pd.DataFrame,
    last_refreshed_date
):
    st.caption(f"Last refreshed: {last_refreshed_date.strftime('%Y-%m-%d')}")
    st.markdown("**Executive Summary:** High-level synthesis of adoption velocity, training coverage, and operational readiness.")
    st.markdown(
        "Use this view to brief leadership on the overall health of the AI enablement initiative. Indicators track the conversion of 'activity' (attendance) into 'institutional capacity' (readiness)."
    )
    render_overview_section(adoption_overall, coverage_rate, avg_completion, total_attendance)
    top_ready = (
        readiness_df.sort_values("current_readiness_score", ascending=False).head(1)["department_name"].iloc[0]
        if not readiness_df.empty
        else "N/A"
    )
    conf_delta = impact_summary_df["delta"].mean() if not impact_summary_df.empty else 0
    exec_notes = [
        f"**Readiness Leader:** {top_ready} exhibits highest composite readiness; recommend engaging leadership for peer-mentoring pilot.",
        f"**Competency Shift:** +{conf_delta:.2f} net gain in confidence metrics post-intervention; validates current curriculum effectiveness.",
        f"**Capacity Signal:** {total_attendance:,} total engagements recorded; align facilitator staffing to sustain support for high-velocity periods.",
    ]
    render_executive_notes(exec_notes)
    st.download_button(
        "Download overview metrics (CSV)",
        data=readiness_df.to_csv(index=False),
        file_name="overview_readiness.csv",
        mime="text/csv",
    )

def render_adoption_tab(adoption_df: pd.DataFrame, readiness_df: pd.DataFrame):
    st.markdown(
        "Comparative analysis of departmental readiness profiles. Identifies units that are well-positioned for advanced AI integration versus those requiring foundational support. Use these metrics to allocate resources and identify peer-mentoring opportunities."
    )
    render_adoption_section(adoption_df)
    st.dataframe(
        adoption_df.sort_values("adoption_index", ascending=False).rename(
            columns={"department_name": "Department", "adoption_index": "Adoption Index"}
        ),
        use_container_width=True,
        hide_index=True,
    )
    render_department_readiness_section(readiness_df)
    st.download_button(
        "Download adoption & readiness data (CSV)",
        data=adoption_df.merge(readiness_df, on=["department_id", "department_name"], how="left").to_csv(index=False),
        file_name="adoption_readiness.csv",
        mime="text/csv",
    )

def render_learning_impact_tab(impact_summary_df: pd.DataFrame):
    st.markdown(
        "Longitudinal assessment of confidence and competency shifts. Validates whether training interventions are driving measurable improvements in responsible AI understanding across faculty, staff, and graduate student cohorts."
    )
    render_learning_impact_section(impact_summary_df)
    st.download_button(
        "Download learning impact (CSV)",
        data=impact_summary_df.to_csv(index=False),
        file_name="learning_impact.csv",
        mime="text/csv",
    )

def render_engagement_tab(
    timeseries_df: pd.DataFrame,
    by_format_df: pd.DataFrame,
    by_audience_df: pd.DataFrame,
    completion_df: pd.DataFrame
):
    st.markdown(
        "Temporal analysis of participation volume and modality preferences. Supports capacity planning, facilitator staffing, and the optimization of workshop formats to maximize institutional reach."
    )
    render_participation_section(timeseries_df, by_format_df, by_audience_df, completion_df)
    st.download_button(
        "Download engagement data (CSV)",
        data=timeseries_df.to_csv(index=False),
        file_name="engagement_timeseries.csv",
        mime="text/csv",
    )

def render_reflections_tab(sentiment_df: pd.DataFrame, theme_df: pd.DataFrame):
    st.markdown(
        "Thematic analysis of qualitative feedback. Surfaces emerging risks, ethical concerns, and support needs reported by participants. These signals are critical for guiding policy adjustments and curriculum refinement."
    )
    render_reflection_section(sentiment_df, theme_df)
    st.download_button(
        "Download reflections summary (CSV)",
        data=theme_df.to_csv(index=False),
        file_name="reflections_themes.csv",
        mime="text/csv",
    )

def render_department_focus_tab(
    departments: pd.DataFrame,
    selected_depts: List[str],
    adoption_df: pd.DataFrame,
    readiness_df: pd.DataFrame,
    filtered_workshops: pd.DataFrame,
    participants: pd.DataFrame,
    reflections: pd.DataFrame,
    role_filter: List[str],
    audience_filter: List[str]
):
    st.markdown(
        "Detailed unit-level reporting for chair briefings and strategic planning. Provides a granular view of adoption, readiness, and engagement for a specific department."
    )
    focus_options = selected_depts if selected_depts else list(departments["department_id"])
    focus_dept = st.selectbox(
        "Department in focus",
        options=focus_options,
        format_func=lambda x: departments.set_index("department_id").loc[x, "department_name"],
    )
    focus_name = departments.set_index("department_id").loc[focus_dept, "department_name"]
    dept_adopt = adoption_df[adoption_df["department_id"] == focus_dept]
    dept_ready = readiness_df[readiness_df["department_id"] == focus_dept]
    
    dept_engagement = compute_workshop_engagement(
        filter_by_departments(filtered_workshops, "department_id", [focus_dept]),
        [focus_dept],
        audience_filter,
    )
    dept_timeseries = dept_engagement["timeseries"]
    
    reflections_with_dept = reflections.merge(
        participants[["participant_id", "department_id", "role"]], on="participant_id", how="left"
    )
    dept_reflection = compute_reflection_sentiment(
        filter_by_departments(reflections_with_dept, "department_id", [focus_dept]),
        participants,
        filtered_department_ids=[focus_dept],
        filtered_roles=role_filter,
    )
    dept_themes = dept_reflection["themes"]
    
    render_department_focus(focus_name, dept_adopt, dept_ready, dept_timeseries, dept_themes)
    st.download_button(
        "Download department snapshot (CSV)",
        data=dept_ready.to_csv(index=False),
        file_name=f"{focus_dept}_snapshot.csv",
        mime="text/csv",
    )
