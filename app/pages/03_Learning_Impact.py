import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import plotly.graph_objects as go
from app.layout import render_header, render_footer, render_sidebar_filters, apply_filters
from app.data_loader import load_all_data
from app.kpi_calculations import calculate_confidence_deltas

render_header()

st.title("Learning Impact")

# Load all data
data = load_all_data()

# Render sidebar filters and get selections
filters = render_sidebar_filters(data["departments"])

# Apply filters to data
filtered_data = apply_filters(data, filters)

# Display filter info
if len(filters["departments"]) < len(data["departments"]["department_name"].unique()):
    st.info(f"📊 Showing data for {len(filters['departments'])} department(s)")

st.subheader("Confidence Shifts (Pre vs Post)")

deltas = calculate_confidence_deltas(filtered_data["assessments_pre"], filtered_data["assessments_post"])

# Radar Chart for Deltas
categories = [
    "Confidence AI Tools", 
    "Pedagogical Use", 
    "Risk Mitigation", 
    "Overall Readiness"
]
values = [
    deltas["confidence_ai_tools_delta"],
    deltas["confidence_pedagogical_use_delta"],
    deltas["confidence_risk_mitigation_delta"],
    deltas["overall_readiness_delta"]
]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Improvement Delta'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 2]
        )),
    showlegend=False,
    title="Average Improvement Delta by Category"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Detailed Metrics")
st.dataframe(deltas.to_frame(name="Average Improvement"))

render_footer()
