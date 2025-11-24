import pandas as pd
import pytest
from app.kpi_calculations import calculate_participation_metrics, calculate_confidence_deltas

def test_participation_metrics():
    df = pd.DataFrame({
        "registrations": [10, 20],
        "attended": [8, 15]
    })
    metrics = calculate_participation_metrics(df)
    assert metrics["total_registrations"] == 30
    assert metrics["total_attended"] == 23
    assert metrics["total_workshops"] == 2

def test_confidence_deltas():
    pre = pd.DataFrame({
        "person_id": ["1", "2"],
        "workshop_id": ["A", "A"],
        "confidence_ai_tools": [1, 2],
        "confidence_pedagogical_use": [1, 1],
        "confidence_risk_mitigation": [1, 1],
        "overall_readiness": [1, 1]
    })
    post = pd.DataFrame({
        "person_id": ["1", "2"],
        "workshop_id": ["A", "A"],
        "confidence_ai_tools": [3, 4], # +2, +2
        "confidence_pedagogical_use": [2, 2],
        "confidence_risk_mitigation": [2, 2],
        "overall_readiness": [2, 2]
    })
    
    deltas = calculate_confidence_deltas(pre, post)
    assert deltas["confidence_ai_tools_delta"] == 2.0
