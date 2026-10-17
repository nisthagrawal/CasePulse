import pytest
import pandas as pd
from analytics.duration_engine import calculate_event_durations
from analytics.case_metrics import generate_case_metrics

def test_calculate_event_durations():
    events_data = [
        {"case_identifier": "WPCRL/1/2026", "cnr": "UKHC01", "event_date": "2026-02-12", "event_type": "Hearing"},
        {"case_identifier": "WPCRL/1/2026", "cnr": "UKHC01", "event_date": "2026-02-18", "event_type": "Hearing"},
        {"case_identifier": "WPCRL/1/2026", "cnr": "UKHC01", "event_date": "2026-03-16", "event_type": "Order"}
    ]
    df_events = pd.DataFrame(events_data)
    durations = calculate_event_durations(df_events)
    
    assert len(durations) == 2
    # 12 Feb -> 18 Feb = 6 days
    assert durations.iloc[0]["duration_days"] == 6
    # 18 Feb -> 16 Mar = 26 days
    assert durations.iloc[1]["duration_days"] == 26

def test_generate_case_metrics():
    cases_data = [{
        "case_identifier": "WPCRL/1/2026", "cnr": "UKHC01", "case_type": "WPCRL",
        "case_year": "2026", "status": "Disposed",
        "filing_date": "2026-01-01", "decision_date": "2026-03-16"
    }]
    events_data = [
        {"case_identifier": "WPCRL/1/2026", "cnr": "UKHC01", "event_date": "2026-02-12", "event_type": "Hearing"},
        {"case_identifier": "WPCRL/1/2026", "cnr": "UKHC01", "event_date": "2026-03-16", "event_type": "Order"}
    ]
    durations_data = [{
        "case_identifier": "WPCRL/1/2026", "cnr": "UKHC01", "duration_days": 32
    }]
    
    df_cases = pd.DataFrame(cases_data)
    df_events = pd.DataFrame(events_data)
    df_orders = pd.DataFrame()
    df_durations = pd.DataFrame(durations_data)
    
    metrics = generate_case_metrics(df_cases, df_events, df_orders, df_durations)
    assert len(metrics) == 1
    assert metrics.iloc[0]["total_duration_days"] == 74  # 01-01 to 03-16
    assert metrics.iloc[0]["number_of_events"] == 2
    assert metrics.iloc[0]["median_event_gap_days"] == 32
