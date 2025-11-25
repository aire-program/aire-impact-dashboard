from typing import Dict, List

import pandas as pd
import io
import streamlit as st

from .data_loader import load_all_data, validate_dataframe  # type: ignore


SYNTHETIC = "synthetic"
UPLOADED = "uploaded"

REQUIRED_FILES = {
    "workshops": ("workshops.csv", "workshops_schema.json"),
    "participants": ("participants.csv", "participants_schema.json"),
    "confidence_pre": ("confidence_surveys_pre.csv", "confidence_surveys_schema.json"),
    "confidence_post": ("confidence_surveys_post.csv", "confidence_surveys_schema.json"),
    "reflections": ("reflections.csv", "reflections_schema.json"),
    "departments": ("departments.csv", "departments_schema.json"),
}


def get_available_data_sources() -> List[str]:
    sources = ["Standard Reference Dataset (Synthetic/Anonymized)"]
    if st.session_state.get("uploaded_data"):
        sources.append("Session Upload (Local/Secure)")
    return sources


def _validate_uploaded(df: pd.DataFrame, schema_name: str) -> pd.DataFrame:
    validate_dataframe(df, schema_name)
    return df


def load_data_for_source(source: str) -> Dict[str, pd.DataFrame]:
    if source == SYNTHETIC:
        return load_all_data()

    uploaded = st.session_state.get("uploaded_data")
    if source == UPLOADED and uploaded:
        return uploaded

    st.info("Uploaded dataset not available; reverting to synthetic data.")
    return load_all_data()


def process_uploads(uploaded_files: Dict[str, bytes]) -> Dict[str, pd.DataFrame]:
    """Parse and validate uploaded CSV content into DataFrames."""
    dataframes: Dict[str, pd.DataFrame] = {}
    for key, (filename, schema_name) in REQUIRED_FILES.items():
        if filename not in uploaded_files:
            raise ValueError(f"{filename} is required.")
        uploaded_obj = uploaded_files[filename]
        # st.file_uploader returns UploadedFile; getvalue gives bytes for pandas
        file_bytes = uploaded_obj.getvalue()
        df = pd.read_csv(io.BytesIO(file_bytes))
        _validate_uploaded(df, schema_name)
        dataframes[key] = df
    return dataframes
