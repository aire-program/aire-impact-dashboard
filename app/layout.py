import streamlit as st

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

def render_footer():
    """Renders the standard footer."""
    st.markdown("---")
    st.markdown(
        "**AIRE Program** | Applied AI Innovation & Research Enablement | *Synthetic Data Mirror*"
    )
