import pandas as pd
import numpy as np

def calculate_event_durations(df_events: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates consecutive event gap intervals for every case in df_events.
    Returns DataFrame matching event_durations.csv schema:
    case_identifier, cnr, previous_event_date, current_event_date,
    previous_event_type, current_event_type, duration_days.
    """
    if df_events.empty:
        return pd.DataFrame(columns=[
            "case_identifier", "cnr", "previous_event_date", "current_event_date",
            "previous_event_type", "current_event_type", "duration_days"
        ])

    df = df_events.copy()
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df = df.dropna(subset=["event_date"])
    
    # Sort chronologically per case
    df = df.sort_values(by=["case_identifier", "event_date"])

    durations = []
    
    for (case_id, cnr), group in df.groupby(["case_identifier", "cnr"]):
        if len(group) < 2:
            continue
            
        rows = group.to_dict("records")
        for i in range(1, len(rows)):
            prev = rows[i - 1]
            curr = rows[i]
            
            p_date = prev["event_date"]
            c_date = curr["event_date"]
            
            gap_days = (c_date - p_date).days
            if gap_days >= 0:
                durations.append({
                    "case_identifier": case_id,
                    "cnr": cnr,
                    "previous_event_date": p_date.strftime("%Y-%m-%d"),
                    "current_event_date": c_date.strftime("%Y-%m-%d"),
                    "previous_event_type": prev.get("event_type", ""),
                    "current_event_type": curr.get("event_type", ""),
                    "duration_days": gap_days
                })

    return pd.DataFrame(durations)
