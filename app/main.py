import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.layout import render_header, render_footer

# Redirect to the first page
render_header()

st.title("Applied AI Literacy – Program Impact Dashboard")

st.markdown("""
### Welcome

This dashboard provides a comprehensive view of the impact, adoption, and engagement metrics for the Applied AI Literacy initiative within the AIRE Program at Michigan State University.

**Please select a page from the sidebar to begin.**

#### Available Modules:
- **Overview**: High-level executive summary and KPIs.
- **Adoption & Readiness**: Tracking AI tool usage and readiness across departments.
- **Learning Impact**: Pre/Post assessment analysis and confidence shifts.
- **Engagement & Pathways**: Workshop participation and learner journeys.
- **Reflections & VoC**: Qualitative analysis of participant feedback.
- **Forecasts & Reports**: Predictive modeling for future planning.

*Note: This is a synthetic data mirror for public demonstration.*
""")

render_footer()
