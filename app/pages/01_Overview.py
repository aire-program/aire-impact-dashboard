import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from app.layout import render_header, render_footer, render_sidebar_filters, apply_filters
from app.data_loader import load_all_data
from app.kpi_calculations import calculate_participation_metrics, calculate_confidence_deltas
from app.charts import plot_adoption_trends

render_header()

st.title("Executive Overview")

# Load all data
data = load_all_data()

# Render sidebar filters and get selections
filters = render_sidebar_filters(data["departments"])

# Apply filters to data
filtered_data = apply_filters(data, filters)

# Display filter info
if len(filters["departments"]) < len(data["departments"]["department_name"].unique()):
    st.info(f"📊 Showing data for {len(filters['departments'])} department(s)")

# Top-level Metrics
col1, col2, col3, col4 = st.columns(4)

participation = calculate_participation_metrics(filtered_data["workshops"])
deltas = calculate_confidence_deltas(filtered_data["assessments_pre"], filtered_data["assessments_post"])

with col1:
    st.metric("Total Workshops", participation["total_workshops"])
with col2:
    st.metric("Total Registrations", participation["total_registrations"])
with col3:
    st.metric("Avg Attendance Rate", f"{participation['avg_attendance_rate']:.1f}%")
with col4:
    st.metric("Avg Readiness Gain", f"+{deltas['overall_readiness_delta']:.2f}")

st.markdown("---")

# Main Charts
st.subheader("Adoption Trajectory")
st.plotly_chart(plot_adoption_trends(filtered_data["adoption_events"]), use_container_width=True)

st.markdown("### Key Insights")
st.info("""
- **Participation** remains strong with consistent attendance rates.
- **Readiness** scores show a positive trend post-intervention.
- **Adoption** events are increasing, indicating practical application of skills.
""")

render_footer()
