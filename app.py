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
        "Data context",
        options=data_source_options,
        format_func=lambda x: "Standard Reference Dataset (Synthetic/Anonymized)" if x == SYNTHETIC else "Session Upload (Local/Secure)",
        index=data_source_options.index(st.session_state["active_source"]) if st.session_state["active_source"] in data_source_options else 0,
    )
    st.session_state["active_source"] = selected_source
    st.sidebar.caption("Reference synthetic dataset contains no institutional records; uploaded data remains local to this session.")
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
    source_label = "Reference synthetic dataset (no institutional records)" if selected_source == SYNTHETIC else "Session upload (local memory only)"
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
        st.markdown("**Strategic Value:** High-level synthesis of adoption velocity, coverage equity, and operational readiness.")
        st.markdown(
            "Use this view to brief leadership on the overall health of the AI enablement initiative. Indicators focus on the conversion of 'activity' (attendance) into 'capacity' (readiness)."
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
    with tabs[1]:
        st.markdown(
            "Departmental adoption and readiness indicators. Identify prepared vs. at-risk units for responsible AI use. Direct support to departments below coverage/readiness targets; replicate practices from leaders."
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
    with tabs[2]:
        st.markdown(
            "Pre/post confidence and responsible AI understanding. Validate training effectiveness across faculty, staff, and graduate students. Adjust modality and follow-on supports based on observed gains."
        )
        render_learning_impact_section(impact_summary_df)
        st.download_button(
            "Download learning impact (CSV)",
            data=impact_summary_df.to_csv(index=False),
            file_name="learning_impact.csv",
            mime="text/csv",
        )
    with tabs[3]:
        st.markdown(
            "Participation over time and by format/audience. Optimize scheduling, facilitator load, and modality investments. Align facilitators to peak months and formats that sustain completion and reach priority audiences."
        )
        render_participation_section(timeseries_df, by_format_df, by_audience_df, completion_df)
        st.download_button(
            "Download engagement data (CSV)",
            data=timeseries_df.to_csv(index=False),
            file_name="engagement_timeseries.csv",
            mime="text/csv",
        )
    with tabs[4]:
        st.markdown(
            "Themed qualitative reflections with sentiment. Surface early signals on adoption, risks, and support needs that quantitative metrics may miss. Address recurring themes (ethical concerns, assessment) with targeted guidance and governance updates."
        )
        render_reflection_section(sentiment_df, theme_df)
        st.download_button(
            "Download reflections summary (CSV)",
            data=theme_df.to_csv(index=False),
            file_name="reflections_themes.csv",
            mime="text/csv",
        )
    with tabs[5]:
        st.markdown(
            "Targeted snapshot for the selected department to brief chairs and associate deans. Calibrate supports, monitor readiness and coverage targets, and track participation demand."
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


if __name__ == "__main__":
    main()
