import json
from pathlib import Path
from typing import Dict

import pandas as pd
from jsonschema import Draft7Validator

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"
SCHEMA_DIR = BASE_DIR / "schemas"


def _read_schema(schema_name: str) -> Draft7Validator:
    schema_path = SCHEMA_DIR / schema_name
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return Draft7Validator(schema)


def _load_and_validate(csv_name: str, schema_name: str, date_cols=None) -> pd.DataFrame:
    csv_path = DATA_DIR / csv_name
    df = pd.read_csv(csv_path)
    validator = _read_schema(schema_name)

    records = df.to_dict(orient="records")
    for idx, record in enumerate(records):
        errors = sorted(validator.iter_errors(record), key=lambda e: e.path)
        if errors:
            messages = "; ".join([f"{'.'.join(map(str, e.path))}: {e.message}" for e in errors])
            raise ValueError(f"Validation failed for {csv_name} at row {idx}: {messages}")

    if date_cols:
        for col in date_cols:
            df[col] = pd.to_datetime(df[col])
    return df


def validate_dataframe(df: pd.DataFrame, schema_name: str) -> None:
    """
    Validate an in-memory DataFrame against a JSON schema.
    Raises ValueError with details if validation fails.
    """
    validator = _read_schema(schema_name)
    records = df.to_dict(orient="records")
    for idx, record in enumerate(records):
        errors = sorted(validator.iter_errors(record), key=lambda e: e.path)
        if errors:
            messages = "; ".join([f"{'.'.join(map(str, e.path))}: {e.message}" for e in errors])
            raise ValueError(f"Validation failed for {schema_name} at row {idx}: {messages}")


def load_workshops() -> pd.DataFrame:
    return _load_and_validate(
        "workshops.csv",
        "workshops_schema.json",
        date_cols=["date"],
    )


def load_participants() -> pd.DataFrame:
    return _load_and_validate(
        "participants.csv",
        "participants_schema.json",
        date_cols=["last_attended_date"],
    )


def load_confidence_surveys_pre() -> pd.DataFrame:
    return _load_and_validate(
        "confidence_surveys_pre.csv",
        "confidence_surveys_schema.json",
        date_cols=["date"],
    )


def load_confidence_surveys_post() -> pd.DataFrame:
    return _load_and_validate(
        "confidence_surveys_post.csv",
        "confidence_surveys_schema.json",
        date_cols=["date"],
    )


def load_reflections() -> pd.DataFrame:
    return _load_and_validate(
        "reflections.csv",
        "reflections_schema.json",
        date_cols=["date"],
    )


def load_departments() -> pd.DataFrame:
    return _load_and_validate("departments.csv", "departments_schema.json")


def load_all_data() -> Dict[str, pd.DataFrame]:
    workshops = load_workshops()
    participants = load_participants()
    conf_pre = load_confidence_surveys_pre()
    conf_post = load_confidence_surveys_post()
    reflections = load_reflections()
    departments = load_departments()
    return {
        "workshops": workshops,
        "participants": participants,
        "confidence_pre": conf_pre,
        "confidence_post": conf_post,
        "reflections": reflections,
        "departments": departments,
    }
