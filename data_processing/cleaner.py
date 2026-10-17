import re
from datetime import datetime
import pandas as pd

def normalize_date(date_str: str) -> str:
    """
    Normalizes arbitrary date strings (e.g., '12-02-2026', '12/02/2026', '2026-02-12', '12-Feb-2026')
    to standard ISO format YYYY-MM-DD.
    Returns empty string if invalid or unavailable.
    """
    if not date_str or pd.isna(date_str):
        return ""
    
    date_str = str(date_str).strip()
    if not date_str:
        return ""

    formats = [
        "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y",
        "%d-%b-%Y", "%d %b %Y", "%d-%B-%Y", "%Y/%m/%d"
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
            
    # Try regex fallback for DD-MM-YYYY
    match = re.search(r'(\d{2})[-/.](\d{2})[-/.](\d{4})', date_str)
    if match:
        day, month, year = match.groups()
        try:
            dt = datetime(int(year), int(month), int(day))
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return ""

def clean_text(text: str) -> str:
    """
    Trims extra whitespace and normalizes text fields.
    """
    if not text or pd.isna(text):
        return ""
    text = str(text).strip()
    return re.sub(r'\s+', ' ', text)

def clean_cases_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans cases DataFrame: normalizes dates and text fields.
    """
    if df.empty:
        return df

    date_cols = ["filing_date", "registration_date", "decision_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = df[col].apply(normalize_date)

    text_cols = ["case_identifier", "case_type", "case_number", "case_year", "petitioner", "respondent", "judge", "status"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    return df

def clean_events_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans case events DataFrame.
    """
    if df.empty:
        return df

    if "event_date" in df.columns:
        df["event_date"] = df["event_date"].apply(normalize_date)

    text_cols = ["case_identifier", "event_type", "purpose", "judge", "remarks"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    return df

def clean_orders_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans orders DataFrame.
    """
    if df.empty:
        return df

    if "order_date" in df.columns:
        df["order_date"] = df["order_date"].apply(normalize_date)

    text_cols = ["case_identifier", "case_type", "case_number", "order_number"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    return df
