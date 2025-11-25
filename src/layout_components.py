import streamlit as st
import plotly.express as px
from typing import List

from .charts import (
    PALETTE,
    make_adoption_radar_chart,
    make_confidence_change_chart,
    make_department_readiness_scatter,
    make_overview_kpi_cards,
    make_reflection_sentiment_bar,
    make_theme_distribution_bar,
    make_workshop_engagement_timeseries,
)

FONT_FAMILY = "'IBM Plex Sans', 'Inter', system-ui, -apple-system, sans-serif"

LUCIDE_ICONS = {
    "target": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><circle cx='12' cy='12' r='6'/><circle cx='12' cy='12' r='2'/></svg>",
    "spark": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M5 3v4'/><path d='M19 17v4'/><path d='M3 5h4'/><path d='M17 19h4'/><path d='m6.5 6.5 3 3'/><path d='m14.5 14.5 3 3'/><path d='M10 2h4'/><path d='M10 22h4'/><path d='m7 7 2-2'/><path d='m15 15 2-2'/></svg>",
    "notes": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M19 21H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l6 6v10a2 2 0 0 1-2 2Z'/><path d='M14 3v4a2 2 0 0 0 2 2h4'/><path d='M9 15h6'/><path d='M9 19h6'/></svg>",
    "chart": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 3v18h18'/><path d='M7 13l3-3 4 4 5-5'/></svg>",
    "building": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 21h18'/><path d='M6 21V7l6-4 6 4v14'/><path d='M9 21v-6h6v6'/></svg>",
}


def inject_styles():
    st.markdown(
        f"""
        <style>
        :root {{
            --primary: {PALETTE["primary"]};
            --primary-dark: {PALETTE["primary_dark"]};
            --accent: {PALETTE["accent"]};
            --soft: {PALETTE["soft"]};
            --muted: {PALETTE["muted"]};
        }}
        html, body, [class*="css"]  {{
            font-family: {FONT_FAMILY};
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 700;
            color: var(--primary-dark);
        }}
        /* Tag chips */
        div[data-baseweb="tag"], span[data-baseweb="tag"] {{
            background-color: var(--soft) !important;
            color: var(--primary-dark) !important;
            border: 1px solid #9bc7b3 !important;
        }}
        .stMultiSelect [data-baseweb="tag"] svg {{
            color: var(--primary-dark) !important;
        }}
        /* Top banner */
        .aire-banner {{
            background: var(--primary-dark);
            color: #f2fbff;
            padding: 14px 18px;
            border-radius: 12px;
            margin-bottom: 12px;
        }}
        .aire-banner strong {{ color: #f2fbff; }}
        .metric-card-title {{
            display: flex; gap: 6px; align-items: center;
            font-weight: 600;
            color: var(--primary-dark);
        }}
        .stTabs [role="tablist"] button {{
            background: transparent;
            border: none;
            color: var(--primary-dark);
            padding: 8px 12px;
            border-radius: 0;
            margin-right: 6px;
            box-shadow: none;
        }}
        .stTabs [role="tablist"] button[aria-selected="true"] {{
            background: transparent;
            border: none;
            color: var(--primary);
            box-shadow: inset 0 -2px 0 0 var(--primary);
        }}
        .stTabs [role="tablist"] button:hover {{
            background: transparent;
            border: none;
            color: var(--primary);
            box-shadow: inset 0 -2px 0 0 #b7dbe8;
        }}
        .stMetric > div {{
            background: #ffffff;
            border: 1px solid #e2ebf0;
            border-radius: 12px;
            padding: 8px 10px;
        }}
        .executive-card {{
            background:#f7fbfd;
            border:1px solid #dbe9f1;
            border-radius:12px;
            padding:14px 16px;
        }}
        .lucide {{ display:inline-flex; vertical-align:middle; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    inject_styles()
    st.markdown(
        f"""
        <div class="aire-banner">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                <div style="display:flex;gap:10px;align-items:center;">
                    <span class="lucide">{LUCIDE_ICONS["building"]}</span>
                    <div>
                        <div style="font-size:18px;font-weight:700;letter-spacing:0.2px;">AIRE Impact Dashboard</div>
                        <div style="font-size:13px;opacity:0.9;">Applied AI Innovation & Research Enablement (AIRE) | College of Social Science | Michigan State University</div>
                    </div>
                </div>
                <div style="font-size:12px;opacity:0.9;">Leadership-facing view of AIRE literacy, readiness, and responsible AI adoption</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_filters(all_departments_df, all_roles_list, default_date_range):
    st.sidebar.header("Decision Filters")
    st.sidebar.write(
        "Adjust the institutional view by date, department, and audience to understand reach, readiness, and equity of access."
    )
    start_default, end_default = default_date_range
    date_range = st.sidebar.date_input("Workshop date window", value=(start_default, end_default))
    selected_depts = st.sidebar.multiselect(
        "Departments to analyze",
        options=all_departments_df["department_id"],
        format_func=lambda x: all_departments_df.set_index("department_id").loc[x, "department_name"],
        default=list(all_departments_df["department_id"]),
    )
    selected_roles = st.sidebar.multiselect(
        "Faculty and staff segments",
        options=all_roles_list,
        default=all_roles_list,
        help="Focus on specific user groups to gauge adoption equity and confidence shifts.",
    )
    return date_range, selected_depts, selected_roles


def render_overview_section(adoption_overall, coverage_rate, avg_completion, total_attendance):
    st.subheader("Overview")
    st.write(
        "Core signals from the Applied AI Innovation & Research Enablement (AIRE) Program—adoption strength, training coverage, completion, and participation volume. Chairs, associate deans, and program directors use this view weekly to verify reach, benchmark momentum, and confirm coverage targets. Interpret movements alongside filters to see how departmental selections and audience focus shift institutional readiness."
    )
    cards = make_overview_kpi_cards(adoption_overall, coverage_rate, avg_completion, total_attendance)
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        col.metric(card["label"], card["value"], help=card["help"])


def render_adoption_section(dept_adoption_df):
    st.subheader("AI Adoption & Readiness")
    st.write(
        "Composite adoption index combining readiness, training coverage, and participant adoption levels across departments. Highlights where responsible AI use is stabilizing, where uptake is uneven, and where stewardship attention is needed. Compare departments to identify outliers; values are scaled 0–100 to support goal-setting and peer benchmarking."
    )
    fig = make_adoption_radar_chart(dept_adoption_df)
    st.plotly_chart(fig, use_container_width=True)


def render_learning_impact_section(impact_summary_df):
    st.subheader("Learning Outcomes & Confidence")
    st.write(
        "Movement in confidence and responsible AI understanding before and after AIRE learning interventions. Confirms whether training is increasing responsible AI competency for faculty, staff, and graduate students. Track pre/post averages and deltas; sustained gains signal effective design, while flat lines flag the need for targeted reinforcement."
    )
    fig = make_confidence_change_chart(impact_summary_df)
    st.plotly_chart(fig, use_container_width=True)


def render_participation_section(timeseries_df, by_format_df, by_audience_df, completion_df):
    st.subheader("Participation & Engagement")
    st.write(
        "Participation trends by month, learning format, and audience segment. Guides scheduling, facilitator load, and modality investments to meet demand equitably. Use the time series to spot surges; format and audience breakouts reveal where coverage is strong and where additional outreach is needed."
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
            px.bar(by_format_df, x="format", y="attendances", title="Engagement by Format", color_discrete_sequence=[PALETTE["primary"]]),
            use_container_width=True,
        )
    if by_audience_df.empty:
        col4.info("No data for this selection")
    else:
        col4.plotly_chart(
            px.bar(by_audience_df, x="audience", y="attendances", title="Engagement by Audience", color_discrete_sequence=[PALETTE["accent"]]),
            use_container_width=True,
        )


def render_reflection_section(sentiment_df, theme_df):
    st.subheader("Reflections & Sentiment")
    st.write(
        "Themed reflections with sentiment to capture qualitative signals about responsible AI practice, risk posture, and support needs. Complements quantitative KPIs with lived experience from faculty, staff, and graduate students—critical for governance and equity monitoring. Review dominant themes and sentiment mix to target guidance, policy reinforcement, or follow-up consultations."
    )
    col1, col2 = st.columns(2)
    col1.plotly_chart(make_reflection_sentiment_bar(sentiment_df), use_container_width=True)
    col2.plotly_chart(make_theme_distribution_bar(theme_df), use_container_width=True)


def render_department_readiness_section(readiness_df):
    st.subheader("Department Readiness Matrix")
    st.write(
        "Readiness versus coverage with participant volume context for each department. Shows whether training reach is translating into operational readiness and where gaps remain. Use bubble size for participation scale; compare to targets to prioritize direct support or peer mentoring."
    )
    fig = make_department_readiness_scatter(readiness_df)
    st.plotly_chart(fig, use_container_width=True)


def render_department_focus(dept_name: str, adoption_df, readiness_df, timeseries_df, themes_df):
    st.markdown(f"### {dept_name} Focus")
    st.write(
        "Targeted view for this department: adoption strength, readiness posture, and engagement signals to brief chairs and associate deans."
    )
    col1, col2 = st.columns(2)
    if not adoption_df.empty:
        col1.dataframe(adoption_df[["department_name", "adoption_index"]].rename(columns={"department_name": "Department", "adoption_index": "Adoption Index"}), use_container_width=True, hide_index=True)
    if not readiness_df.empty:
        col2.dataframe(
            readiness_df[["department_name", "training_coverage_rate", "current_readiness_score", "participant_count"]].rename(
                columns={
                    "department_name": "Department",
                    "training_coverage_rate": "Coverage",
                    "current_readiness_score": "Readiness",
                    "participant_count": "Participants",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    st.plotly_chart(make_workshop_engagement_timeseries(timeseries_df), use_container_width=True)
    st.plotly_chart(make_theme_distribution_bar(themes_df), use_container_width=True)


def render_executive_notes(notes: List[str]):
    st.markdown(
        f"""
        <div class="executive-card">
            <div class="metric-card-title"><span class="lucide">{LUCIDE_ICONS["notes"]}</span>Executive Notes</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for note in notes:
        st.markdown(f"- {note}")
