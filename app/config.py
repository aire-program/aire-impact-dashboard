import os

APP_TITLE = "Applied AI Literacy – Program Impact Dashboard"
APP_VERSION = "1.0.0"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dummy")

DEPARTMENTS_FILE = os.path.join(DATA_DIR, "departments.csv")
WORKSHOPS_FILE = os.path.join(DATA_DIR, "workshops.csv")
ASSESSMENTS_PRE_FILE = os.path.join(DATA_DIR, "assessments_pre.csv")
ASSESSMENTS_POST_FILE = os.path.join(DATA_DIR, "assessments_post.csv")
ADOPTION_EVENTS_FILE = os.path.join(DATA_DIR, "adoption_events.csv")
REFLECTIONS_FILE = os.path.join(DATA_DIR, "reflections.csv")

# Color Palette
COLOR_PRIMARY = "#18453B"  # MSU Green-ish
COLOR_SECONDARY = "#00818A"
COLOR_ACCENT = "#FFB81C"

# Chart Config
PLOTLY_THEME = "plotly_white"
