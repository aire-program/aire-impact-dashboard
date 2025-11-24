import streamlit as st
import pandas as pd

def render_header():
    """Renders the standard header."""
    st.set_page_config(
        page_title="AIRE Impact Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.sidebar.title("Navigation")
    st.sidebar.info(
        "**Applied AI Literacy – Program Impact Dashboard**\n\n"
        "College of Social Science\n"
        "Michigan State University"
    )

def render_sidebar_filters(departments_df: pd.DataFrame) -> dict:
    """
    Renders sidebar filtering controls and returns selected filter values.
    
    Args:
        departments_df: DataFrame containing department information
        
    Returns:
        Dictionary with selected filter values
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters")
    
    # Get unique values for filters
    all_departments = sorted(departments_df['department_name'].unique().tolist())
    all_divisions = sorted(departments_df['division'].unique().tolist())
    all_size_bands = sorted(departments_df['size_band'].unique().tolist())
    
    # Department filter
    selected_departments = st.sidebar.multiselect(
        "Departments",
        options=all_departments,
        default=all_departments,
        help="Select one or more departments to filter data"
    )
    
    # Division filter
    selected_divisions = st.sidebar.multiselect(
        "Divisions",
        options=all_divisions,
        default=all_divisions,
        help="Filter by academic division"
    )
    
    # Size band filter
    selected_size_bands = st.sidebar.multiselect(
        "Department Size",
        options=all_size_bands,
        default=all_size_bands,
        help="Filter by department size"
    )
    
    # Reset filters button
    if st.sidebar.button("Reset All Filters"):
        st.rerun()
    
    return {
        "departments": selected_departments,
        "divisions": selected_divisions,
        "size_bands": selected_size_bands
    }

def apply_filters(data: dict, filters: dict) -> dict:
    """
    Applies filters to all datasets based on selected departments.
    
    Args:
        data: Dictionary of DataFrames
        filters: Dictionary of filter selections
        
    Returns:
        Filtered dictionary of DataFrames
    """
    # Filter departments
    filtered_depts = data["departments"][
        (data["departments"]["department_name"].isin(filters["departments"])) &
        (data["departments"]["division"].isin(filters["divisions"])) &
        (data["departments"]["size_band"].isin(filters["size_bands"]))
    ]
    
    filtered_dept_ids = filtered_depts["department_id"].tolist()
    
    # Apply filters to other datasets
    filtered_data = {
        "departments": filtered_depts
    }
    
    # Filter workshops if department_id exists
    if "workshops" in data and "department_id" in data["workshops"].columns:
        filtered_data["workshops"] = data["workshops"][
            data["workshops"]["department_id"].isin(filtered_dept_ids)
        ]
    else:
        filtered_data["workshops"] = data["workshops"]
    
    # Filter assessments if participant_id can be linked to departments
    # For now, pass through assessments as-is (can be enhanced with participant linking)
    filtered_data["assessments_pre"] = data["assessments_pre"]
    filtered_data["assessments_post"] = data["assessments_post"]
    
    # Filter adoption events if department_id exists
    if "adoption_events" in data and "department_id" in data["adoption_events"].columns:
        filtered_data["adoption_events"] = data["adoption_events"][
            data["adoption_events"]["department_id"].isin(filtered_dept_ids)
        ]
    else:
        filtered_data["adoption_events"] = data["adoption_events"]
    
    # Filter reflections if department_id exists
    if "reflections" in data and "department_id" in data["reflections"].columns:
        filtered_data["reflections"] = data["reflections"][
            data["reflections"]["department_id"].isin(filtered_dept_ids)
        ]
    else:
        filtered_data["reflections"] = data["reflections"]
    
    return filtered_data

def render_footer():
    """Renders the standard footer."""
    st.markdown("---")
    st.markdown(
        "**AIRE Program** | Applied AI Innovation & Research Enablement | *Synthetic Data Mirror*"
    )
