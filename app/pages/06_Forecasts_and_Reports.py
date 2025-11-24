import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from app.layout import render_header, render_footer
from app.data_loader import load_all_data
from app.kpi_calculations import forecast_registrations

render_header()

st.title("Forecasts & Reports")

data = load_all_data()

st.subheader("Registration Forecast (Next 3 Months)")
forecast = forecast_registrations(data["workshops"])

if forecast:
    forecast_df = pd.DataFrame(forecast, columns=["Date", "Predicted Registrations"])
    
    # Combine with historical
    historical = data["workshops"][["date", "registrations"]].copy()
    historical.columns = ["Date", "Registrations"]
    historical["Type"] = "Historical"
    
    forecast_df.columns = ["Date", "Registrations"]
    forecast_df["Type"] = "Forecast"
    
    combined = pd.concat([historical, forecast_df])
    
    fig = px.line(
        combined, 
        x="Date", 
        y="Registrations", 
        color="Type", 
        title="Registration Trends and Forecast",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Not enough data to generate a forecast.")

st.subheader("Strategic Narrative")
st.markdown("""
Based on current trends, we anticipate a **steady increase** in demand for AI literacy workshops. 
Departments with lower baseline readiness are showing the highest engagement growth, suggesting that 
outreach efforts are effective. 

**Recommendations:**
1. Increase capacity for 'Intro' level workshops.
2. Target 'Humanities' division for specialized 'Ethics' tracks.
3. Monitor adoption risk flags in 'Research' contexts.
""")

render_footer()
