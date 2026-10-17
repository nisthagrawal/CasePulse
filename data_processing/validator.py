import pandas as pd
from typing import Tuple, List

EXPECTED_CASE_FIELDS = [
    "cnr", "case_identifier", "case_number", "case_type", "case_year",
    "filing_number", "filing_date", "registration_number", "registration_date",
    "status", "decision_date", "petitioner", "respondent",
    "petitioner_advocate", "respondent_advocate", "court_number", "judge", "source_url"
]

EXPECTED_EVENT_FIELDS = [
    "event_id", "cnr", "case_identifier", "case_number",
    "event_date", "event_type", "purpose", "court_number", "judge", "remarks", "source_url"
]

EXPECTED_ORDER_FIELDS = [
    "order_id", "cnr", "case_identifier", "case_type", "case_number", "case_year",
    "order_date", "order_number", "order_url", "source_url", "search_from_date", "search_to_date"
]

def validate_cases(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    missing = [f for f in EXPECTED_CASE_FIELDS if f not in df.columns]
    if missing:
        return False, [f"Missing expected case fields: {missing}"]
    return True, []

def validate_events(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    missing = [f for f in EXPECTED_EVENT_FIELDS if f not in df.columns]
    if missing:
        return False, [f"Missing expected event fields: {missing}"]
    return True, []

def validate_orders(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    missing = [f for f in EXPECTED_ORDER_FIELDS if f not in df.columns]
    if missing:
        return False, [f"Missing expected order fields: {missing}"]
    return True, []
