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
    render_department_readiness_section,
    render_header,
    render_learning_impact_section,
    render_overview_section,
    render_participation_section,
    render_reflection_section,
    render_sidebar_filters,
)


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

    render_overview_section(adoption_overall, coverage_rate, avg_completion, total_attendance)
    render_adoption_section(adoption_df)
    render_learning_impact_section(impact_summary_df)
    render_participation_section(timeseries_df, by_format_df, by_audience_df, completion_df)
    render_reflection_section(sentiment_df, theme_df)
    render_department_readiness_section(readiness_df)


if __name__ == "__main__":
    main()
