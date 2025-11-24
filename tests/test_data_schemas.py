import pytest
import pandas as pd
import json
import os
from jsonschema import validate

DATA_DIR = "data/dummy"
SCHEMA_DIR = "data/schemas"

def load_schema(name):
    # Map pre/post assessments to the single assessments schema
    if name.startswith("assessments_"):
        schema_name = "assessments"
    else:
        schema_name = name
        
    with open(os.path.join(SCHEMA_DIR, f"{schema_name}.schema.json")) as f:
        return json.load(f)

def load_csv(name):
    return pd.read_csv(os.path.join(DATA_DIR, f"{name}.csv"))

@pytest.mark.parametrize("name", [
    "departments",
    "workshops",
    "assessments_pre",
    "assessments_post",
    "adoption_events",
    "reflections"
])
def test_csv_schema_validation(name):
    """Validates each CSV row against its JSON schema."""
    df = load_csv(name)
    schema = load_schema(name)
    
    # Replace NaN with None for JSON compatibility
    df = df.astype(object).where(pd.notnull(df), None)
    
    # Convert DataFrame to list of dicts for validation
    records = df.to_dict(orient="records")
    
    for record in records:
        # Validate each record
        validate(instance=record, schema=schema)
