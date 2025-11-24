import plotly.express as px
import streamlit as st

from .charts import (
    make_adoption_radar_chart,
    make_confidence_change_chart,
    make_department_readiness_scatter,
    make_overview_kpi_cards,
    make_reflection_sentiment_bar,
    make_theme_distribution_bar,
    make_workshop_engagement_timeseries,
)


def render_header():
    st.title("AIRE Impact Dashboard (Synthetic Data)")
    st.caption(
        "Applied AI Innovation & Research Enablement | Michigan State University | Synthetic, non-production mirror"
    )


def render_sidebar_filters(all_departments_df, all_roles_list, default_date_range):
    st.sidebar.header("Filters")
    start_default, end_default = default_date_range
    date_range = st.sidebar.date_input("Workshop date range", value=(start_default, end_default))
    selected_depts = st.sidebar.multiselect(
        "Departments",
        options=all_departments_df["department_id"],
        format_func=lambda x: all_departments_df.set_index("department_id").loc[x, "department_name"],
        default=list(all_departments_df["department_id"]),
    )
    selected_roles = st.sidebar.multiselect("User groups", options=all_roles_list, default=all_roles_list)
    return date_range, selected_depts, selected_roles


def render_overview_section(adoption_overall, coverage_rate, avg_completion, total_attendance):
    st.subheader("Overview")
    st.write(
        "WHAT: Quick view of the program's footprint, completion, and adoption. "
        "WHY: Leadership can see immediate progress and relative momentum. "
        "HOW: Cards respond to filters for department and audience."
    )
    cards = make_overview_kpi_cards(adoption_overall, coverage_rate, avg_completion, total_attendance)
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        col.metric(card["label"], card["value"], help=card["help"])


def render_adoption_section(dept_adoption_df):
    st.subheader("AI Adoption & Readiness")
    st.write(
        "WHAT: Composite adoption index blending readiness, training coverage, and participant adoption levels. "
        "WHY: Signals where departments are accelerating or need support. "
        "HOW: Radar chart compares selected departments; index scales 0–100."
    )
    fig = make_adoption_radar_chart(dept_adoption_df)
    st.plotly_chart(fig, use_container_width=True)


def render_learning_impact_section(impact_summary_df):
    st.subheader("Learning Outcomes & Confidence")
    st.write(
        "WHAT: Change in self-reported confidence and responsible AI understanding before vs. after sessions. "
        "WHY: Gauges learning effectiveness for audiences and departments. "
        "HOW: Bars show pre/post averages; positive deltas indicate improved confidence."
    )
    fig = make_confidence_change_chart(impact_summary_df)
    st.plotly_chart(fig, use_container_width=True)


def render_participation_section(timeseries_df, by_format_df, by_audience_df, completion_df):
    st.subheader("Participation & Engagement")
    st.write(
        "WHAT: Attendance over time and by format/audience. "
        "WHY: Identifies demand patterns, preferred formats, and surge moments. "
        "HOW: Lines show monthly attendance; bars break down format and audience volume."
    )
    col1, col2 = st.columns([2, 1])
    col1.plotly_chart(make_workshop_engagement_timeseries(timeseries_df), use_container_width=True)
    with col2:
        if completion_df.empty:
            st.info("No data for this selection")
        else:
            st.metric("Average Completion", f"{completion_df['value'].iloc[0]*100:.0f}%")

    col3, col4 = st.columns(2)
    if by_format_df.empty:
        col3.info("No data for this selection")
    else:
        col3.plotly_chart(
            px.bar(by_format_df, x="format", y="attendances", title="Engagement by Format"),
            use_container_width=True,
        )
    if by_audience_df.empty:
        col4.info("No data for this selection")
    else:
        col4.plotly_chart(
            px.bar(by_audience_df, x="audience", y="attendances", title="Engagement by Audience"),
            use_container_width=True,
        )


def render_reflection_section(sentiment_df, theme_df):
    st.subheader("Reflections & Sentiment")
    st.write(
        "WHAT: Participant reflections themed by use case with sentiment distribution. "
        "WHY: Surfaces qualitative signals on adoption, risks, and support needs. "
        "HOW: Bars show sentiment mix and dominant themes for the selection."
    )
    col1, col2 = st.columns(2)
    col1.plotly_chart(make_reflection_sentiment_bar(sentiment_df), use_container_width=True)
    col2.plotly_chart(make_theme_distribution_bar(theme_df), use_container_width=True)


def render_department_readiness_section(readiness_df):
    st.subheader("Department Readiness Matrix")
    st.write(
        "WHAT: Scatter of readiness vs. coverage with participant volume. "
        "WHY: Highlights where adoption work is translating into readiness gains. "
        "HOW: Bubble size approximates participant volume; use filters to isolate departments."
    )
    fig = make_department_readiness_scatter(readiness_df)
    st.plotly_chart(fig, use_container_width=True)
