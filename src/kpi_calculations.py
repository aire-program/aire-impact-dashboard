from typing import Dict, Iterable, Optional, Tuple

import numpy as np
import pandas as pd

from .filters import filter_by_departments, filter_by_roles


ADOPTION_MAPPING = {"early": 0.3, "developing": 0.6, "established": 1.0}


def _maybe_filter(df: pd.DataFrame, dept_col: str, department_ids: Optional[Iterable[str]]) -> pd.DataFrame:
    return filter_by_departments(df, dept_col, department_ids)


def compute_ai_adoption_index(
    departments_df: pd.DataFrame,
    participants_df: pd.DataFrame,
    filtered_department_ids: Optional[Iterable[str]] = None,
) -> Tuple[pd.DataFrame, float]:
    dept_df = _maybe_filter(departments_df, "department_id", filtered_department_ids)
    participant_subset = _maybe_filter(participants_df, "department_id", filtered_department_ids)

    if participant_subset.empty or dept_df.empty:
        return pd.DataFrame(columns=["department_id", "department_name", "adoption_index"]), 0.0

    participant_subset = participant_subset.assign(adoption_numeric=participant_subset["adoption_level"].map(ADOPTION_MAPPING))
    adoption_by_dept = participant_subset.groupby("department_id")["adoption_numeric"].mean().reset_index()

    merged = dept_df.merge(adoption_by_dept, on="department_id", how="left").fillna({"adoption_numeric": 0})
    merged["adoption_index"] = (
        (merged["current_readiness_score"] * 0.4)
        + (merged["training_coverage_rate"] * 0.35)
        + (merged["adoption_numeric"] * 0.25)
    ) * 100
    merged["adoption_index"] = merged["adoption_index"].round(1)

    overall = merged["adoption_index"].mean().round(1) if not merged.empty else 0.0
    return merged[["department_id", "department_name", "adoption_index"]], overall


def compute_learning_impact(
    conf_pre_df: pd.DataFrame,
    conf_post_df: pd.DataFrame,
    participants_df: pd.DataFrame,
    filtered_department_ids: Optional[Iterable[str]] = None,
    filtered_roles: Optional[Iterable[str]] = None,
) -> Dict[str, pd.DataFrame]:
    pre = conf_pre_df.merge(participants_df[["participant_id", "department_id", "role"]], on="participant_id", how="left")
    post = conf_post_df.merge(participants_df[["participant_id", "department_id", "role"]], on="participant_id", how="left")

    pre = _maybe_filter(pre, "department_id", filtered_department_ids)
    post = _maybe_filter(post, "department_id", filtered_department_ids)
    pre = filter_by_roles(pre, "role", filtered_roles)
    post = filter_by_roles(post, "role", filtered_roles)

    def _impact_summary(df_pre: pd.DataFrame, df_post: pd.DataFrame) -> pd.DataFrame:
        if df_pre.empty or df_post.empty:
            return pd.DataFrame(
                columns=[
                    "group",
                    "metric",
                    "pre_mean",
                    "post_mean",
                    "delta",
                    "effect_size",
                ]
            )
        merged_local = df_pre.merge(df_post, on=["participant_id", "workshop_id"], suffixes=("_pre", "_post"))
        if merged_local.empty:
            return pd.DataFrame(columns=["group", "metric", "pre_mean", "post_mean", "delta", "effect_size"])

        metrics = ["confidence_score", "understanding_responsible_ai"]
        rows = []
        for metric in metrics:
            pre_vals = merged_local[f"{metric}_pre"].astype(float)
            post_vals = merged_local[f"{metric}_post"].astype(float)
            pre_mean = pre_vals.mean()
            post_mean = post_vals.mean()
            delta = post_mean - pre_mean
            pooled_std = np.sqrt(((pre_vals.std(ddof=1) ** 2) + (post_vals.std(ddof=1) ** 2)) / 2)
            effect_size = delta / pooled_std if pooled_std > 0 else 0
            rows.append(
                {
                    "group": "overall",
                    "metric": metric,
                    "pre_mean": round(pre_mean, 2),
                    "post_mean": round(post_mean, 2),
                    "delta": round(delta, 2),
                    "effect_size": round(effect_size, 2),
                }
            )
        return pd.DataFrame(rows)

    summary_df = _impact_summary(pre, post)

    def _breakdown(group_field: str) -> pd.DataFrame:
        if pre.empty or post.empty:
            return pd.DataFrame(columns=[group_field, "metric", "delta"])
        merged_local = pre.merge(post, on=["participant_id", "workshop_id"], suffixes=("_pre", "_post"))
        if merged_local.empty:
            return pd.DataFrame(columns=[group_field, "metric", "delta"])
        if "department_id_pre" in merged_local.columns:
            merged_local["department_id"] = merged_local.get("department_id_pre").fillna(
                merged_local.get("department_id_post")
            )
        if "role_pre" in merged_local.columns:
            merged_local["role"] = merged_local.get("role_pre").fillna(merged_local.get("role_post"))
        if group_field not in merged_local.columns:
            return pd.DataFrame(columns=[group_field, "metric", "delta"])
        records = []
        for group_value, group_df in merged_local.groupby(group_field):
            for metric in ["confidence_score", "understanding_responsible_ai"]:
                pre_vals = group_df[f"{metric}_pre"].astype(float)
                post_vals = group_df[f"{metric}_post"].astype(float)
                delta = post_vals.mean() - pre_vals.mean()
                records.append(
                    {
                        group_field: group_value,
                        "metric": metric,
                        "delta": round(delta, 2),
                        "post_mean": round(post_vals.mean(), 2),
                        "pre_mean": round(pre_vals.mean(), 2),
                    }
                )
        return pd.DataFrame(records)

    by_department = _breakdown("department_id")
    by_role = _breakdown("role")

    return {
        "summary": summary_df,
        "by_department": by_department,
        "by_role": by_role,
    }


def compute_training_coverage(
    departments_df: pd.DataFrame, filtered_department_ids: Optional[Iterable[str]] = None
) -> Tuple[pd.DataFrame, float]:
    df = _maybe_filter(departments_df, "department_id", filtered_department_ids)
    if df.empty:
        return pd.DataFrame(columns=["department_id", "department_name", "training_coverage_rate"]), 0.0
    aggregate = round(df["training_coverage_rate"].mean(), 2)
    return df[["department_id", "department_name", "training_coverage_rate"]], aggregate


def compute_workshop_engagement(
    workshops_df: pd.DataFrame,
    filtered_department_ids: Optional[Iterable[str]] = None,
    filtered_audiences: Optional[Iterable[str]] = None,
) -> Dict[str, pd.DataFrame]:
    df = _maybe_filter(workshops_df, "department_id", filtered_department_ids)
    if filtered_audiences:
        df = df[df["audience"].isin(filtered_audiences)]
    if df.empty:
        return {
            "timeseries": pd.DataFrame(columns=["month", "attendances"]),
            "by_format": pd.DataFrame(columns=["format", "attendances"]),
            "by_audience": pd.DataFrame(columns=["audience", "attendances"]),
            "completion": pd.DataFrame(columns=["metric", "value"]),
        }

    timeseries = df.copy()
    timeseries["month"] = timeseries["date"].dt.to_period("M").dt.to_timestamp()
    timeseries = timeseries.groupby("month")["attendances"].sum().reset_index()

    by_format = df.groupby("format")["attendances"].sum().reset_index()
    by_audience = df.groupby("audience")["attendances"].sum().reset_index()
    completion = pd.DataFrame(
        {
            "metric": ["average_completion"],
            "value": [round(df["completion_rate"].mean(), 2)],
        }
    )

    return {
        "timeseries": timeseries,
        "by_format": by_format,
        "by_audience": by_audience,
        "completion": completion,
    }


def compute_reflection_sentiment(
    reflections_df: pd.DataFrame,
    participants_df: pd.DataFrame,
    filtered_department_ids: Optional[Iterable[str]] = None,
    filtered_roles: Optional[Iterable[str]] = None,
) -> Dict[str, pd.DataFrame]:
    merged = reflections_df.merge(
        participants_df[["participant_id", "department_id", "role"]], on="participant_id", how="left"
    )
    merged = _maybe_filter(merged, "department_id", filtered_department_ids)
    merged = filter_by_roles(merged, "role", filtered_roles)

    if merged.empty:
        return {
            "sentiment": pd.DataFrame(columns=["sentiment", "count"]),
            "themes": pd.DataFrame(columns=["theme", "count"]),
        }

    sentiment = merged.groupby("sentiment").size().reset_index(name="count")
    themes = merged.groupby("theme").size().reset_index(name="count")
    return {"sentiment": sentiment, "themes": themes}


def compute_readiness_matrix(
    departments_df: pd.DataFrame, filtered_department_ids: Optional[Iterable[str]] = None
) -> pd.DataFrame:
    df = _maybe_filter(departments_df, "department_id", filtered_department_ids)
    if df.empty:
        return pd.DataFrame(
            columns=[
                "department_id",
                "department_name",
                "training_coverage_rate",
                "current_readiness_score",
                "participant_count",
            ]
        )
    df = df.copy()
    # lightweight synthetic participant count for bubble sizing
    df["participant_count"] = np.random.randint(80, 260, size=len(df))
    return df[
        [
            "department_id",
            "department_name",
            "training_coverage_rate",
            "current_readiness_score",
            "participant_count",
        ]
    ]
