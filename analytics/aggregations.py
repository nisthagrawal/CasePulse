import pandas as pd
from typing import Dict, Any

def get_summary_kpis(df_cases: pd.DataFrame, df_events: pd.DataFrame, df_orders: pd.DataFrame, df_metrics: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes top-level KPI summary statistics.
    """
    total_cases = len(df_cases) if not df_cases.empty else 0
    pending_cases = len(df_cases[df_cases["status"] == "Pending"]) if not df_cases.empty else 0
    disposed_cases = len(df_cases[df_cases["status"] == "Disposed"]) if not df_cases.empty else 0
    total_events = len(df_events) if not df_events.empty else 0
    total_orders = len(df_orders) if not df_orders.empty else 0

    median_duration = 0.0
    if not df_metrics.empty and "total_duration_days" in df_metrics.columns:
        valid_durations = df_metrics["total_duration_days"].dropna()
        if not valid_durations.empty:
            median_duration = float(valid_durations.median())

    return {
        "total_cases": total_cases,
        "pending_cases": pending_cases,
        "disposed_cases": disposed_cases,
        "total_events": total_events,
        "total_orders": total_orders,
        "median_observed_duration": round(median_duration, 1)
    }

def get_cases_by_type(df_cases: pd.DataFrame) -> pd.DataFrame:
    if df_cases.empty or "case_type" not in df_cases.columns:
        return pd.DataFrame(columns=["case_type", "count"])
    return df_cases["case_type"].value_counts().reset_index().rename(columns={"index": "case_type", "case_type": "count"})

def get_cases_by_year(df_cases: pd.DataFrame) -> pd.DataFrame:
    if df_cases.empty or "case_year" not in df_cases.columns:
        return pd.DataFrame(columns=["case_year", "count"])
    return df_cases["case_year"].value_counts().sort_index().reset_index().rename(columns={"index": "case_year", "case_year": "count"})

def get_orders_by_month(df_orders: pd.DataFrame) -> pd.DataFrame:
    if df_orders.empty or "order_date" not in df_orders.columns:
        return pd.DataFrame(columns=["year_month", "count"])
    
    df = df_orders.copy()
    df["dt"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["year_month"] = df["dt"].dt.to_period("M").astype(str)
    return df["year_month"].value_counts().sort_index().reset_index().rename(columns={"index": "year_month", "order_date": "count"})
