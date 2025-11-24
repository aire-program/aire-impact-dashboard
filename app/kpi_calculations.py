import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_participation_metrics(workshops_df: pd.DataFrame) -> dict:
    """Calculates total workshops, registrations, and attendance."""
    return {
        "total_workshops": len(workshops_df),
        "total_registrations": workshops_df["registrations"].sum(),
        "total_attended": workshops_df["attended"].sum(),
        "avg_attendance_rate": (workshops_df["attended"].sum() / workshops_df["registrations"].sum()) * 100 if workshops_df["registrations"].sum() > 0 else 0
    }

def calculate_confidence_deltas(pre_df: pd.DataFrame, post_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the average improvement in confidence scores."""
    # Merge on assessment_id or person/workshop combo. 
    # Since assessment_ids are unique per row, we merge on person_id and workshop_id.
    merged = pd.merge(
        pre_df, 
        post_df, 
        on=["person_id", "workshop_id"], 
        suffixes=("_pre", "_post")
    )
    
    metrics = [
        "confidence_ai_tools",
        "confidence_pedagogical_use",
        "confidence_risk_mitigation",
        "overall_readiness"
    ]
    
    deltas = {}
    for m in metrics:
        deltas[f"{m}_delta"] = merged[f"{m}_post"] - merged[f"{m}_pre"]
        
    delta_df = pd.DataFrame(deltas)
    return delta_df.mean()

def calculate_department_readiness(departments_df: pd.DataFrame, assessments_post_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates readiness scores by department."""
    dept_scores = assessments_post_df.groupby("department_id")["overall_readiness"].mean().reset_index()
    merged = pd.merge(departments_df, dept_scores, on="department_id", how="left")
    merged["overall_readiness"] = merged["overall_readiness"].fillna(0)
    return merged

def forecast_registrations(workshops_df: pd.DataFrame, periods=3) -> list:
    """Simple linear regression forecast for registrations."""
    df = workshops_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["ordinal_date"] = df["date"].map(pd.Timestamp.toordinal)
    
    X = df[["ordinal_date"]].values
    y = df["registrations"].values
    
    if len(X) < 2:
        return []

    model = LinearRegression()
    model.fit(X, y)
    
    last_date = df["date"].max()
    future_dates = [last_date + pd.Timedelta(days=30 * i) for i in range(1, periods + 1)]
    future_ordinals = [[d.toordinal()] for d in future_dates]
    
    predictions = model.predict(future_ordinals)
    return list(zip(future_dates, predictions))
