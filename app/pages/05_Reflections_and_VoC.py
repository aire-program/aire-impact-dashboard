import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from app.layout import render_header, render_footer
from app.data_loader import load_all_data
from app.charts import plot_sentiment_breakdown

render_header()

st.title("Reflections & Voice of Community")

data = load_all_data()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Sentiment Analysis")
    st.plotly_chart(plot_sentiment_breakdown(data["reflections"]), use_container_width=True)

with col2:
    st.subheader("Recent Reflections")
    for _, row in data["reflections"].sample(5).iterrows():
        with st.expander(f"{row['role'].title()} - {row['theme'].title()}"):
            st.write(f"**Sentiment:** {row['sentiment']}")
            st.write(f"_{row['reflection_text']}_")

render_footer()
