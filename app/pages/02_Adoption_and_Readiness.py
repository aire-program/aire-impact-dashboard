import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import plotly.express as px
from app.layout import render_header, render_footer
from app.data_loader import load_all_data
from app.kpi_calculations import calculate_department_readiness

render_header()

st.title("Adoption & Readiness")

data = load_all_data()

st.subheader("Departmental Readiness")
dept_readiness = calculate_department_readiness(data["departments"], data["assessments_post"])

fig_dept = px.bar(
    dept_readiness.sort_values("overall_readiness", ascending=True),
    x="overall_readiness",
    y="department_name",
    orientation="h",
    title="Average Post-Workshop Readiness by Department",
    color="overall_readiness",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_dept, use_container_width=True)

st.subheader("Adoption Intensity by Context")
fig_context = px.box(
    data["adoption_events"],
    x="context",
    y="intensity",
    color="context",
    title="Adoption Intensity Distribution by Context"
)
st.plotly_chart(fig_context, use_container_width=True)

render_footer()
