import json
from pathlib import Path

import pandas as pd
from jsonschema import Draft7Validator


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"
SCHEMA_DIR = BASE_DIR / "schemas"


def _validate_file(csv_name: str, schema_name: str):
    df = pd.read_csv(DATA_DIR / csv_name)
    with open(SCHEMA_DIR / schema_name, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft7Validator(schema)
    for idx, record in df.iterrows():
        errors = list(validator.iter_errors(record.to_dict()))
        assert not errors, f"Validation errors in {csv_name} row {idx}: {errors}"


def test_workshops_schema_valid():
    _validate_file("workshops.csv", "workshops_schema.json")


def test_participants_schema_valid():
    _validate_file("participants.csv", "participants_schema.json")


def test_confidence_schema_valid():
    _validate_file("confidence_surveys_pre.csv", "confidence_surveys_schema.json")
    _validate_file("confidence_surveys_post.csv", "confidence_surveys_schema.json")


def test_reflections_schema_valid():
    _validate_file("reflections.csv", "reflections_schema.json")


def test_departments_schema_valid():
    _validate_file("departments.csv", "departments_schema.json")
