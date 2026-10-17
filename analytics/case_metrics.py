import pandas as pd
import numpy as np
from datetime import datetime

def generate_case_metrics(df_cases: pd.DataFrame, df_events: pd.DataFrame, df_orders: pd.DataFrame, df_durations: pd.DataFrame, as_of_date: str = None) -> pd.DataFrame:
    """
    Computes case-level aggregated metrics for case_metrics.csv.
    Stores as_of_date explicitly for reproducible pending case age calculations.
    """
    if df_cases.empty:
        return pd.DataFrame()

    if not as_of_date:
        as_of_dt = datetime.now()
        as_of_date = as_of_dt.strftime("%Y-%m-%d")
    else:
        as_of_dt = pd.to_datetime(as_of_date)

    metrics = []

    event_counts = df_events.groupby("case_identifier").size().to_dict() if not df_events.empty else {}
    order_counts = df_orders.groupby("case_identifier").size().to_dict() if not df_orders.empty else {}

    for _, case in df_cases.iterrows():
        case_id = case.get("case_identifier", "")
        cnr = case.get("cnr", "")
        case_type = case.get("case_type", "")
        case_year = case.get("case_year", "")
        status = case.get("status", "Pending")

        filing_str = case.get("filing_date", "")
        decision_str = case.get("decision_date", "")

        filing_dt = pd.to_datetime(filing_str, errors="coerce") if filing_str else None
        decision_dt = pd.to_datetime(decision_str, errors="coerce") if decision_str else None

        total_duration = np.nan
        current_age = np.nan

        if status == "Disposed" and pd.notna(filing_dt) and pd.notna(decision_dt):
            total_duration = max(0, (decision_dt - filing_dt).days)
        elif status == "Pending" and pd.notna(filing_dt):
            current_age = max(0, (as_of_dt - filing_dt).days)

        case_ev = df_events[df_events["case_identifier"] == case_id] if not df_events.empty else pd.DataFrame()
        n_events = len(case_ev)
        n_orders = order_counts.get(case_id, 0)

        first_ev_date = ""
        last_ev_date = ""
        avg_gap = np.nan
        med_gap = np.nan
        max_gap = np.nan

        if not case_ev.empty:
            ev_dates = pd.to_datetime(case_ev["event_date"], errors="coerce").dropna().sort_values()
            if not ev_dates.empty:
                first_ev_date = ev_dates.iloc[0].strftime("%Y-%m-%d")
                last_ev_date = ev_dates.iloc[-1].strftime("%Y-%m-%d")

        if not df_durations.empty:
            case_dur = df_durations[df_durations["case_identifier"] == case_id]
            if not case_dur.empty:
                gaps = case_dur["duration_days"].dropna()
                if not gaps.empty:
                    avg_gap = round(float(gaps.mean()), 2)
                    med_gap = round(float(gaps.median()), 2)
                    max_gap = round(float(gaps.max()), 2)

        metrics.append({
            "case_identifier": case_id,
            "cnr": cnr,
            "case_type": case_type,
            "case_year": case_year,
            "status": status,
            "filing_date": filing_str if pd.notna(filing_str) else "",
            "decision_date": decision_str if pd.notna(decision_str) else "",
            "total_duration_days": total_duration,
            "current_age_days": current_age,
            "number_of_events": n_events,
            "number_of_orders": n_orders,
            "first_event_date": first_ev_date,
            "last_event_date": last_ev_date,
            "average_event_gap_days": avg_gap,
            "median_event_gap_days": med_gap,
            "maximum_event_gap_days": max_gap,
            "as_of_date": as_of_date
        })

    return pd.DataFrame(metrics)
