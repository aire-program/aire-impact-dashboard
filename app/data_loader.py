import pandas as pd
import os
from app.config import (
    DEPARTMENTS_FILE,
    WORKSHOPS_FILE,
    ASSESSMENTS_PRE_FILE,
    ASSESSMENTS_POST_FILE,
    ADOPTION_EVENTS_FILE,
    REFLECTIONS_FILE
)

def load_departments() -> pd.DataFrame:
    """Loads departments data."""
    if not os.path.exists(DEPARTMENTS_FILE):
        raise FileNotFoundError(f"File not found: {DEPARTMENTS_FILE}")
    return pd.read_csv(DEPARTMENTS_FILE)

def load_workshops() -> pd.DataFrame:
    """Loads workshops data."""
    if not os.path.exists(WORKSHOPS_FILE):
        raise FileNotFoundError(f"File not found: {WORKSHOPS_FILE}")
    return pd.read_csv(WORKSHOPS_FILE)

def load_assessments_pre() -> pd.DataFrame:
    """Loads pre-assessments data."""
    if not os.path.exists(ASSESSMENTS_PRE_FILE):
        raise FileNotFoundError(f"File not found: {ASSESSMENTS_PRE_FILE}")
    return pd.read_csv(ASSESSMENTS_PRE_FILE)

def load_assessments_post() -> pd.DataFrame:
    """Loads post-assessments data."""
    if not os.path.exists(ASSESSMENTS_POST_FILE):
        raise FileNotFoundError(f"File not found: {ASSESSMENTS_POST_FILE}")
    return pd.read_csv(ASSESSMENTS_POST_FILE)

def load_adoption_events() -> pd.DataFrame:
    """Loads adoption events data."""
    if not os.path.exists(ADOPTION_EVENTS_FILE):
        raise FileNotFoundError(f"File not found: {ADOPTION_EVENTS_FILE}")
    return pd.read_csv(ADOPTION_EVENTS_FILE)

def load_reflections() -> pd.DataFrame:
    """Loads reflections data."""
    if not os.path.exists(REFLECTIONS_FILE):
        raise FileNotFoundError(f"File not found: {REFLECTIONS_FILE}")
    return pd.read_csv(REFLECTIONS_FILE)

def load_all_data():
    """Loads all datasets into a dictionary."""
    return {
        "departments": load_departments(),
        "workshops": load_workshops(),
        "assessments_pre": load_assessments_pre(),
        "assessments_post": load_assessments_post(),
        "adoption_events": load_adoption_events(),
        "reflections": load_reflections()
    }
