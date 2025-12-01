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
    render_data_management_panel,
)
from src.charts import PALETTE
from src.data_sources import (
    SYNTHETIC,
    UPLOADED,
    get_available_data_sources,
    load_data_for_source,
    process_uploads,
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


from src.views import (
    render_adoption_tab,
    render_department_focus_tab,
    render_engagement_tab,
    render_learning_impact_tab,
    render_overview_tab,
    render_reflections_tab,
)

def main():
    st.set_page_config(page_title="AIRE Impact Dashboard", layout="wide")
    if "active_source" not in st.session_state:
        st.session_state["active_source"] = SYNTHETIC
    if "uploaded_data" not in st.session_state:
        st.session_state["uploaded_data"] = None
    if "view" not in st.session_state:
        st.session_state["view"] = "dashboard"
    if "trigger_validation" not in st.session_state:
        st.session_state["trigger_validation"] = False

    if st.session_state.get("trigger_validation"):
        try:
            files = st.session_state.get("uploaded_raw", {})
            if files:
                uploaded_data = process_uploads(files)
                st.session_state["uploaded_data"] = uploaded_data
                st.session_state["active_source"] = UPLOADED
                st.session_state["upload_status"] = "Uploaded data are now in use for this session."
                st.success("Uploaded data validated and loaded. Dashboard is now using session uploads.")
            else:
                st.error("No files found for validation.")
        except Exception as e:
            st.session_state["active_source"] = SYNTHETIC
            st.session_state["upload_status"] = f"Validation failed: {e}"
            st.error(f"Validation failed: {e}")
        finally:
            st.session_state["trigger_validation"] = False

    data_source_options = [SYNTHETIC]
    if st.session_state.get("uploaded_data"):
        data_source_options.append(UPLOADED)
    selected_source = st.sidebar.selectbox(
        "Data Source Context",
        options=data_source_options,
        format_func=lambda x: "Reference Synthetic Set (Non-Production)" if x == SYNTHETIC else "Session Upload (Secure/Local)",
        index=data_source_options.index(st.session_state["active_source"]) if st.session_state["active_source"] in data_source_options else 0,
    )
    st.session_state["active_source"] = selected_source
    st.sidebar.caption("Note: The reference dataset is synthetically generated to mirror institutional patterns without exposing private records.")
    if st.session_state.get("upload_status"):
        st.sidebar.info(st.session_state["upload_status"])

    data = load_data_for_source(selected_source)
    workshops = data["workshops"]
    participants = data["participants"]
    conf_pre = data["confidence_pre"]
    conf_post = data["confidence_post"]
    reflections = data["reflections"]
    departments = data["departments"]

    last_refreshed = (
        workshops["date"].max().strftime("%Y-%m-%d") if not workshops.empty else "N/A"
    )
    source_label = "Reference Synthetic Data (Non-Production)" if selected_source == SYNTHETIC else "Session Upload (Local Memory Only)"
    render_header(source_label, last_refreshed, view=st.session_state["view"])

    if st.session_state["view"] == "data_management":
        render_data_management_panel()
        return

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
    last_refreshed_date = workshops["date"].max()

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
        render_overview_tab(
            adoption_overall,
            coverage_rate,
            avg_completion,
            total_attendance,
            readiness_df,
            impact_summary_df,
            last_refreshed_date,
        )
    with tabs[1]:
        render_adoption_tab(adoption_df, readiness_df)
    with tabs[2]:
        render_learning_impact_tab(impact_summary_df)
    with tabs[3]:
        render_engagement_tab(timeseries_df, by_format_df, by_audience_df, completion_df)
    with tabs[4]:
        render_reflections_tab(sentiment_df, theme_df)
    with tabs[5]:
        render_department_focus_tab(
            departments,
            selected_depts,
            adoption_df,
            readiness_df,
            filtered_workshops,
            participants,
            reflections,
            role_filter,
            audience_filter,
        )


if __name__ == "__main__":
    main()
