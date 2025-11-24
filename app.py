import streamlit as st

from src.data_loader import load_all_data
from src.filters import filter_by_date_range, filter_by_departments, filter_by_roles
from src.kpi_calculations import (
    compute_ai_adoption_index,
    compute_learning_impact,
    compute_readiness_matrix,
    compute_reflection_sentiment,
    compute_training_coverage,
    compute_workshop_engagement,
)
from src.layout_components import (
    render_adoption_section,
    render_department_focus,
    render_department_readiness_section,
    render_executive_notes,
    render_header,
    render_learning_impact_section,
    render_overview_section,
    render_participation_section,
    render_reflection_section,
    render_sidebar_filters,
)
from src.charts import PALETTE


@st.cache_data
def _load_data():
    return load_all_data()


def _prepare_role_filters(selected_roles):
    if not selected_roles:
        return []
    cleaned = [r for r in selected_roles if r != "mixed"]
    if not cleaned and "mixed" in selected_roles:
        return ["faculty", "staff", "graduate student"]
    return cleaned


def _map_roles_to_audiences(selected_roles):
    if not selected_roles:
        return []
    mapping = {
        "faculty": "faculty",
        "staff": "staff",
        "graduate student": "graduate students",
        "mixed": "mixed",
    }
    return [mapping[r] for r in selected_roles if r in mapping]


def main():
    st.set_page_config(page_title="AIRE Impact Dashboard", layout="wide")
    render_header()

    data = _load_data()
    workshops = data["workshops"]
    participants = data["participants"]
    conf_pre = data["confidence_pre"]
    conf_post = data["confidence_post"]
    reflections = data["reflections"]
    departments = data["departments"]

    all_roles = ["faculty", "staff", "graduate student", "mixed"]
    date_range = (
        workshops["date"].min().date(),
        workshops["date"].max().date(),
    )

    selected_dates, selected_depts, selected_roles = render_sidebar_filters(departments, all_roles, date_range)
    start_date, end_date = selected_dates
    role_filter = _prepare_role_filters(selected_roles)
    audience_filter = _map_roles_to_audiences(selected_roles)

    filtered_workshops = filter_by_departments(
        filter_by_date_range(workshops, "date", start_date, end_date),
        "department_id",
        selected_depts,
    )
    filtered_participants = filter_by_departments(participants, "department_id", selected_depts)
    filtered_participants = filter_by_roles(filtered_participants, "role", role_filter)

    adoption_df, adoption_overall = compute_ai_adoption_index(departments, filtered_participants, selected_depts)
    coverage_df, coverage_overall = compute_training_coverage(departments, selected_depts)
    coverage_rate = coverage_overall

    learning_impact = compute_learning_impact(
        filter_by_date_range(conf_pre, "date", start_date, end_date),
        filter_by_date_range(conf_post, "date", start_date, end_date),
        filtered_participants,
        filtered_department_ids=selected_depts,
        filtered_roles=role_filter,
    )
    impact_summary_df = learning_impact["summary"]

    engagement = compute_workshop_engagement(filtered_workshops, selected_depts, audience_filter)
    timeseries_df = engagement["timeseries"]
    by_format_df = engagement["by_format"]
    by_audience_df = engagement["by_audience"]
    completion_df = engagement["completion"]

    sentiment_theme = compute_reflection_sentiment(
        filter_by_date_range(reflections, "date", start_date, end_date),
        participants,
        filtered_department_ids=selected_depts,
        filtered_roles=role_filter,
    )
    sentiment_df = sentiment_theme["sentiment"]
    theme_df = sentiment_theme["themes"]

    readiness_df = compute_readiness_matrix(departments, selected_depts)

    avg_completion = completion_df["value"].iloc[0] if not completion_df.empty else 0
    total_attendance = int(timeseries_df["attendances"].sum()) if not timeseries_df.empty else 0
    last_refreshed = workshops["date"].max()

    tabs = st.tabs(
        [
            "Overview",
            "Adoption & Readiness",
            "Learning Impact",
            "Engagement",
            "Reflections",
            "Department Focus",
        ]
    )

    with tabs[0]:
        st.caption(f"Last refreshed: {last_refreshed.strftime('%Y-%m-%d')}")
        render_overview_section(adoption_overall, coverage_rate, avg_completion, total_attendance)
        top_ready = (
            readiness_df.sort_values("current_readiness_score", ascending=False).head(1)["department_name"].iloc[0]
            if not readiness_df.empty
            else "N/A"
        )
        conf_delta = impact_summary_df["delta"].mean() if not impact_summary_df.empty else 0
        exec_notes = [
            f"Top readiness: {top_ready}; keep coverage momentum and share playbooks with peers.",
            f"Confidence delta: {conf_delta:.2f} across metrics; reinforce hands-on practice and responsible use norms.",
            f"Attendance total: {total_attendance:,}; align facilitator capacity to peak months and high-demand formats.",
        ]
        render_executive_notes(exec_notes)
        st.download_button(
            "Download overview metrics (CSV)",
            data=readiness_df.to_csv(index=False),
            file_name="overview_readiness.csv",
            mime="text/csv",
        )
    with tabs[1]:
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
    with tabs[2]:
        render_learning_impact_section(impact_summary_df)
        st.download_button(
            "Download learning impact (CSV)",
            data=impact_summary_df.to_csv(index=False),
            file_name="learning_impact.csv",
            mime="text/csv",
        )
    with tabs[3]:
        render_participation_section(timeseries_df, by_format_df, by_audience_df, completion_df)
        st.download_button(
            "Download engagement data (CSV)",
            data=timeseries_df.to_csv(index=False),
            file_name="engagement_timeseries.csv",
            mime="text/csv",
        )
    with tabs[4]:
        render_reflection_section(sentiment_df, theme_df)
        st.download_button(
            "Download reflections summary (CSV)",
            data=theme_df.to_csv(index=False),
            file_name="reflections_themes.csv",
            mime="text/csv",
        )
    with tabs[5]:
        focus_options = selected_depts if selected_depts else list(departments["department_id"])
        focus_dept = st.selectbox(
            "Department to focus",
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


if __name__ == "__main__":
    main()
