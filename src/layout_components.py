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
from .data_sources import REQUIRED_FILES

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
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 10px;
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
            border-radius: 10px;
            padding: 8px 10px;
        }}
        .executive-card {{
            background:#f7fbfd;
            border:1px solid #dbe9f1;
            border-radius:10px;
            padding:14px 16px;
        }}
        .lucide {{ display:inline-flex; vertical-align:middle; }}
        .chip {{
            display:inline-flex;
            align-items:center;
            gap:6px;
            background:#eef6fa;
            color: var(--primary-dark);
            padding:6px 10px;
            border-radius:20px;
            border:1px solid #d2e5ee;
            font-size:12px;
            font-weight:600;
        }}
        .primary-btn {{
            background: {PALETTE["primary"]};
            color:#fff !important;
            padding:8px 14px;
            border-radius:8px;
            border:none;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(active_source: str, last_refreshed: str, view: str = "dashboard"):
    inject_styles()
    st.markdown(
        f"""
        <div class="aire-banner">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                <div style="display:flex;gap:10px;align-items:center;">
                    <span class="lucide">{LUCIDE_ICONS["building"]}</span>
                    <div>
                        <div style="font-size:18px;font-weight:700;letter-spacing:0.2px;">AIRE Impact Dashboard</div>
                        <div style="font-size:13px;opacity:0.9;">Institutional Decision Support | College of Social Science | Michigan State University</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    top_row = st.columns([2, 2, 1])
    with top_row[0]:
        st.caption("Restricted: Institutional Decision Support. Data sensitivity protocols apply.")
    with top_row[1]:
        st.markdown(
            f"""
            <div style="font-size:13px; color: {PALETTE['primary_dark']}; text-align: right;">
                <strong>Data Context:</strong> {active_source} <br>
                <strong>Status:</strong> Live | <strong>Refresh:</strong> {last_refreshed}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_row[2]:
        if view == "data_management":
            if st.button("Back to dashboard", type="primary"):
                st.session_state["view"] = "dashboard"
        else:
            if st.button("Data ingestion & validation", type="primary", help="Manage data ingestion and validation for the dashboard"):
                st.session_state["view"] = "data_management"


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
        key="dept_filter",
    )
    dept_col1, dept_col2 = st.sidebar.columns(2)
    if dept_col1.button("Select all departments"):
        st.session_state["dept_filter"] = list(all_departments_df["department_id"])
        selected_depts = st.session_state["dept_filter"]
    if dept_col2.button("Clear departments"):
        st.session_state["dept_filter"] = []
        selected_depts = []
    st.sidebar.caption(f"Departments selected: {len(selected_depts)}")

    selected_roles = st.sidebar.multiselect(
        "Faculty, staff, and graduate student segments",
        options=all_roles_list,
        default=all_roles_list,
        help="Focus on specific user groups to gauge adoption equity and confidence shifts.",
        key="role_filter",
    )
    role_col1, role_col2 = st.sidebar.columns(2)
    if role_col1.button("Select all roles"):
        st.session_state["role_filter"] = list(all_roles_list)
        selected_roles = st.session_state["role_filter"]
    if role_col2.button("Clear roles"):
        st.session_state["role_filter"] = []
        selected_roles = []
    st.sidebar.caption(f"Roles selected: {len(selected_roles)}")
    return date_range, selected_depts, selected_roles


def render_overview_section(adoption_overall, coverage_rate, avg_completion, total_attendance):
    st.subheader("Executive Summary")
    st.write(
        "Key performance indicators tracking the conversion of enablement activities into institutional capacity. Leadership uses this view to verify reach, benchmark momentum, and confirm coverage targets. Interpret movements alongside filters to see how departmental selections and audience focus shift institutional readiness."
    )
    cards = make_overview_kpi_cards(adoption_overall, coverage_rate, avg_completion, total_attendance)
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        col.metric(card["label"], card["value"], help=card["help"])


def render_adoption_section(dept_adoption_df):
    st.subheader("Departmental Readiness Profile")
    st.write(
        "Integrated view of training coverage, participation depth, and operational maturity. Highlights where responsible AI use is stabilizing versus where stewardship attention is needed. Compare departments to identify outliers; values are scaled 0–100 to support goal-setting."
    )
    fig = make_adoption_radar_chart(dept_adoption_df)
    st.plotly_chart(fig, use_container_width=True)


def render_learning_impact_section(impact_summary_df):
    st.subheader("Competency Growth Analysis")
    st.write(
        "Pre- and post-intervention assessment of responsible AI understanding. Confirms whether training is increasing responsible AI competency for faculty, staff, and graduate students. Sustained gains signal effective design, while flat lines flag the need for targeted reinforcement."
    )
    fig = make_confidence_change_chart(impact_summary_df)
    st.plotly_chart(fig, use_container_width=True)


def render_participation_section(timeseries_df, by_format_df, by_audience_df, completion_df):
    st.subheader("Engagement Velocity")
    st.write(
        "Longitudinal tracking of workshop attendance and modality preferences. Guides scheduling, facilitator load, and modality investments to meet demand equitably. Use the time series to spot surges; format and audience breakouts reveal where coverage is strong and where additional outreach is needed."
    )
    col1, col2 = st.columns([2, 1])
    col1.plotly_chart(make_workshop_engagement_timeseries(timeseries_df), use_container_width=True)
    with col2:
        if completion_df.empty:
            st.info("No data available for the current filters.")
        else:
            st.metric("Average Completion", f"{completion_df['value'].iloc[0]*100:.0f}%")

    col3, col4 = st.columns(2)
    if by_format_df.empty:
        col3.info("No data available for the current filters.")
    else:
        col3.plotly_chart(
            px.bar(by_format_df, x="format", y="attendances", title="Engagement by Format", color_discrete_sequence=[PALETTE["primary"]]),
            use_container_width=True,
        )
    if by_audience_df.empty:
        col4.info("No data available for the current filters.")
    else:
        col4.plotly_chart(
            px.bar(by_audience_df, x="audience", y="attendances", title="Engagement by Audience", color_discrete_sequence=[PALETTE["accent"]]),
            use_container_width=True,
        )


def render_reflection_section(sentiment_df, theme_df):
    st.subheader("Qualitative Intelligence")
    st.write(
        "Thematic analysis of participant feedback and sentiment signals. Complements quantitative KPIs with lived experience from faculty, staff, and graduate students—critical for governance and equity monitoring. Review dominant themes and sentiment mix to target guidance, policy reinforcement, or follow-up consultations."
    )
    col1, col2 = st.columns(2)
    col1.plotly_chart(make_reflection_sentiment_bar(sentiment_df), use_container_width=True)
    col2.plotly_chart(make_theme_distribution_bar(theme_df), use_container_width=True)


def render_department_readiness_section(readiness_df):
    st.subheader("Strategic Alignment Matrix")
    st.write(
        "Evaluating departmental readiness against training penetration. Shows whether training reach is translating into operational readiness and where gaps remain. Use bubble size for participation scale; compare to targets to prioritize direct support or peer mentoring."
    )
    fig = make_department_readiness_scatter(readiness_df)
    st.plotly_chart(fig, use_container_width=True)


def render_department_focus(dept_name: str, adoption_df, readiness_df, timeseries_df, themes_df):
    st.markdown(f"### Unit-Level Intelligence: {dept_name}")
    st.write(
        "Detailed adoption and engagement profile for leadership review. Use this data to inform chair conversations and action plans."
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


def render_data_management_panel():
    st.subheader("Institutional Data Ingestion")
    st.write(
        "Secure validation and loading interface for authorized extracts. This module validates schema conformity before integrating data into the session's analytical context. "
        "Standard operating procedure requires fresh extracts from the AIRE Data Warehouse at the start of each monthly reporting cycle."
    )
    st.info(
        "**Privacy Notice:** Uploaded data is processed locally within the session memory and is never persisted to external storage. "
        "Ensure all PII has been hashed or removed prior to ingestion, per CSS Data Governance Policy 2024-02."
    )

    st.markdown("### Required CSV structure")
    uploaders = {}
    for key, (filename, schema_name) in REQUIRED_FILES.items():
        with st.expander(f"{filename} format and upload", expanded=False):
            if "workshops" in filename:
                st.write(
                    "- workshop_id (string)\n- date (YYYY-MM-DD)\n- title (string)\n- format (workshop, micro-course, webinar, institute)\n- audience (faculty, staff, graduate students, mixed)\n- department_id (string; matches departments.csv)\n- registrations (integer)\n- attendances (integer)\n- completion_rate (0–1)"
                )
            elif "participants" in filename:
                st.write(
                    "- participant_id (string)\n- role (faculty, staff, graduate student)\n- department_id (string)\n- workshops_attended (integer)\n- last_attended_date (YYYY-MM-DD)\n- adoption_level (early, developing, established)\n- ai_confidence_self_rating (1–5)"
                )
            elif "confidence_surveys" in filename:
                st.write(
                    "- survey_id (string)\n- participant_id (string)\n- workshop_id (string)\n- date (YYYY-MM-DD)\n- confidence_score (1–5)\n- understanding_responsible_ai (1–5)\n- comfort_with_tools (1–5)"
                )
            elif "reflections" in filename:
                st.write(
                    "- reflection_id (string)\n- participant_id (string)\n- workshop_id (string)\n- date (YYYY-MM-DD)\n- reflection_text (string)\n- sentiment (positive, neutral, negative)\n- theme (e.g., classroom use, assessment, ethical concerns, research workflows, administrative processes)"
                )
            elif "departments" in filename:
                st.write(
                    "- department_id (string)\n- department_name (string)\n- division (string)\n- baseline_readiness_score (0–1)\n- current_readiness_score (0–1)\n- training_coverage_rate (0–1)"
                )
            uploaders[filename] = st.file_uploader(f"Upload {filename}", type=["csv"], key=f"upload_{filename}")
            if uploaders[filename] is not None:
                st.success(f"{filename} ready for validation.")
            else:
                st.info(f"{filename} not yet provided.")

    all_present = all(uploaders[f] is not None for f in uploaders)

    action_bar = st.container()
    with action_bar:
        col_a, col_b, col_c = st.columns([2, 1, 1])
        with col_a:
            if st.button("Validate and Load Data", disabled=not all_present, type="primary"):
                if not all_present:
                    st.error("All required CSVs must be provided before validation.")
                else:
                    uploaded_files = {name: uploaders[name] for name in uploaders}
                    st.session_state["uploaded_raw"] = uploaded_files
                    st.session_state["trigger_validation"] = True
        with col_b:
            if st.button("Back to dashboard"):
                st.session_state["view"] = "dashboard"
        with col_c:
            if st.button("Return to reference dataset"):
                st.session_state["uploaded_data"] = None
                st.session_state["active_source"] = "synthetic"
                st.success("Dashboard is now using the reference synthetic dataset for this session.")
