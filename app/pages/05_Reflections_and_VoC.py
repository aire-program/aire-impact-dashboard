import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from app.layout import render_header, render_footer, render_sidebar_filters, apply_filters
from app.data_loader import load_all_data
from app.charts import plot_sentiment_breakdown

render_header()

st.title("Reflections & Voice of Community")

# Load all data
data = load_all_data()

# Render sidebar filters and get selections
filters = render_sidebar_filters(data["departments"])

# Apply filters to data
filtered_data = apply_filters(data, filters)

# Display filter info
if len(filters["departments"]) < len(data["departments"]["department_name"].unique()):
    st.info(f"📊 Showing data for {len(filters['departments'])} department(s)")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Sentiment Analysis")
    st.plotly_chart(plot_sentiment_breakdown(filtered_data["reflections"]), use_container_width=True)

with col2:
    st.subheader("Recent Reflections")
    for _, row in filtered_data["reflections"].sample(min(5, len(filtered_data["reflections"]))).iterrows():
        with st.expander(f"{row['role'].title()} - {row['theme'].title()}"):
            st.write(f"**Sentiment:** {row['sentiment']}")
            st.write(f"_{row['reflection_text']}_")

render_footer()
