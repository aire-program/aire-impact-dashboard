import pandas as pd


def filter_by_date_range(df: pd.DataFrame, date_column: str, start_date, end_date) -> pd.DataFrame:
    if start_date is None or end_date is None or date_column not in df.columns:
        return df.copy()
    mask = (df[date_column] >= pd.to_datetime(start_date)) & (df[date_column] <= pd.to_datetime(end_date))
    return df.loc[mask].copy()


def filter_by_departments(df: pd.DataFrame, department_ids_column: str, selected_department_ids) -> pd.DataFrame:
    if not selected_department_ids:
        return df.copy()
    return df[df[department_ids_column].isin(selected_department_ids)].copy()


def filter_by_roles(df: pd.DataFrame, roles_column: str, selected_roles) -> pd.DataFrame:
    if roles_column not in df.columns or not selected_roles:
        return df.copy()
    return df[df[roles_column].isin(selected_roles)].copy()
