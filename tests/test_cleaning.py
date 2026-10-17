import pytest
import pandas as pd
from data_processing.cleaner import normalize_date, clean_text
from data_processing.deduplicator import deduplicate_cases, deduplicate_events, deduplicate_orders

def test_normalize_date():
    assert normalize_date("12-02-2026") == "2026-02-12"
    assert normalize_date("12/02/2026") == "2026-02-12"
    assert normalize_date("2026-02-12") == "2026-02-12"
    assert normalize_date("") == ""
    assert normalize_date(None) == ""

def test_clean_text():
    assert clean_text("  WPCRL /  289  / 2026 ") == "WPCRL / 289 / 2026"
    assert clean_text(None) == ""

def test_deduplicate_cases():
    data = [
        {"cnr": "UKHC01001", "case_identifier": "WPCRL/1/2026", "status": "Pending"},
        {"cnr": "UKHC01001", "case_identifier": "WPCRL/1/2026", "status": "Disposed"}
    ]
    df = pd.DataFrame(data)
    dedup = deduplicate_cases(df)
    assert len(dedup) == 1
    assert dedup.iloc[0]["status"] == "Disposed"

def test_deduplicate_orders():
    data = [
        {"case_identifier": "WPCRL/1/2026", "order_date": "2026-02-12", "order_number": "1"},
        {"case_identifier": "WPCRL/1/2026", "order_date": "2026-02-12", "order_number": "1"}
    ]
    df = pd.DataFrame(data)
    dedup = deduplicate_orders(df)
    assert len(dedup) == 1
