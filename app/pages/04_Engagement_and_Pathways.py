import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from app.layout import render_header, render_footer, render_sidebar_filters, apply_filters
from app.data_loader import load_all_data
from app.charts import plot_registrations_vs_attendance

render_header()

st.title("Engagement & Pathways")

# Load all data
data = load_all_data()

# Render sidebar filters and get selections
filters = render_sidebar_filters(data["departments"])

# Apply filters to data
filtered_data = apply_filters(data, filters)

# Display filter info
if len(filters["departments"]) < len(data["departments"]["department_name"].unique()):
    st.info(f"📊 Showing data for {len(filters['departments'])} department(s)")

st.subheader("Workshop Engagement")
st.plotly_chart(plot_registrations_vs_attendance(filtered_data["workshops"]), use_container_width=True)

st.subheader("Engagement Funnel")
# Simple funnel metrics
total_registrations = filtered_data["workshops"]["registrations"].sum()
total_attended = filtered_data["workshops"]["attended"].sum()
total_adoption_events = len(filtered_data["adoption_events"])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Registrations", total_registrations)
with col2:
    st.metric("Attended", total_attended, delta=f"{total_attended/total_registrations:.1%} conversion")
with col3:
    st.metric("Adoption Events", total_adoption_events, help="Total recorded adoption events post-training")

render_footer()
