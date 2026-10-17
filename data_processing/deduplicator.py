import pandas as pd

def deduplicate_cases(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicates cases by CNR or fallback case_identifier.
    """
    if df.empty:
        return df

    # Create composite fallback key
    df["dedup_key"] = df["cnr"].fillna("")
    mask = df["dedup_key"] == ""
    df.loc[mask, "dedup_key"] = df.loc[mask, "case_identifier"]

    df = df.drop_duplicates(subset=["dedup_key"], keep="last")
    df = df.drop(columns=["dedup_key"])
    return df

def deduplicate_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicates orders by composite key: case_identifier + order_date + order_number.
    """
    if df.empty:
        return df

    df["dedup_key"] = df["case_identifier"].astype(str) + "_" + df["order_date"].astype(str) + "_" + df["order_number"].astype(str)
    df = df.drop_duplicates(subset=["dedup_key"], keep="last")
    df = df.drop(columns=["dedup_key"])
    return df

def deduplicate_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicates events by composite key: case_identifier + event_date + event_type + purpose.
    """
    if df.empty:
        return df

    df["dedup_key"] = (
        df["case_identifier"].astype(str) + "_" +
        df["event_date"].astype(str) + "_" +
        df["event_type"].astype(str) + "_" +
        df["purpose"].astype(str)
    )
    df = df.drop_duplicates(subset=["dedup_key"], keep="last")
    df = df.drop(columns=["dedup_key"])
    return df
