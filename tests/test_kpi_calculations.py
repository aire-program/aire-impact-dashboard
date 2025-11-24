import pandas as pd

from src.data_loader import load_all_data
from src.kpi_calculations import (
    compute_ai_adoption_index,
    compute_learning_impact,
    compute_readiness_matrix,
    compute_reflection_sentiment,
    compute_training_coverage,
    compute_workshop_engagement,
)


def test_adoption_index_ranges():
    data = load_all_data()
    adoption_df, overall = compute_ai_adoption_index(data["departments"], data["participants"])
    assert not adoption_df.empty
    assert adoption_df["adoption_index"].between(0, 100).all()
    assert 0 <= overall <= 100


def test_adoption_single_department():
    data = load_all_data()
    dept_id = [data["departments"]["department_id"].iloc[0]]
    adoption_df, _ = compute_ai_adoption_index(data["departments"], data["participants"], dept_id)
    assert set(adoption_df["department_id"]) == set(dept_id)


def test_learning_impact_filters_roles():
    data = load_all_data()
    dept_ids = data["departments"]["department_id"].head(3).tolist()
    impact = compute_learning_impact(
        data["confidence_pre"],
        data["confidence_post"],
        data["participants"],
        filtered_department_ids=dept_ids,
        filtered_roles=["faculty"],
    )
    summary = impact["summary"]
    if not summary.empty:
        assert (summary["delta"].abs() <= 5).all()


def test_training_coverage_aggregate():
    data = load_all_data()
    _, aggregate = compute_training_coverage(data["departments"])
    assert 0 <= aggregate <= 1


def test_workshop_engagement_output_shapes():
    data = load_all_data()
    engagement = compute_workshop_engagement(data["workshops"])
    assert set(engagement.keys()) == {"timeseries", "by_format", "by_audience", "completion"}
    assert isinstance(engagement["timeseries"], pd.DataFrame)


def test_reflection_sentiment_breakdown():
    data = load_all_data()
    sentiment = compute_reflection_sentiment(
        data["reflections"],
        data["participants"],
        filtered_roles=["graduate student"],
    )
    assert set(sentiment.keys()) == {"sentiment", "themes"}


def test_readiness_matrix_subset():
    data = load_all_data()
    dept_ids = data["departments"]["department_id"].tail(2).tolist()
    readiness = compute_readiness_matrix(data["departments"], dept_ids)
    assert set(readiness["department_id"]) == set(dept_ids)
