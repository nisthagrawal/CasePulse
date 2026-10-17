import os
import pandas as pd
from data_processing.cleaner import clean_cases_dataframe, clean_events_dataframe, clean_orders_dataframe
from data_processing.validator import validate_cases, validate_events, validate_orders
from data_processing.deduplicator import deduplicate_cases, deduplicate_events, deduplicate_orders

class DataPipelineTransformer:
    def __init__(self, raw_dir: str = "data/raw", processed_dir: str = "data/processed", output_dir: str = "output"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.output_dir = output_dir

        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def process_all(self):
        cases_file = os.path.join(self.output_dir, "cases.csv")
        events_file = os.path.join(self.output_dir, "case_events.csv")
        orders_file = os.path.join(self.output_dir, "orders.csv")

        df_cases = pd.read_csv(cases_file) if os.path.exists(cases_file) else pd.DataFrame()
        df_events = pd.read_csv(events_file) if os.path.exists(events_file) else pd.DataFrame()
        df_orders = pd.read_csv(orders_file) if os.path.exists(orders_file) else pd.DataFrame()

        if not df_cases.empty:
            df_cases = clean_cases_dataframe(df_cases)
            df_cases = deduplicate_cases(df_cases)
            df_cases.to_csv(cases_file, index=False)

        if not df_events.empty:
            df_events = clean_events_dataframe(df_events)
            df_events.to_csv(events_file, index=False)

        if not df_orders.empty:
            df_orders = clean_orders_dataframe(df_orders)
            df_orders = deduplicate_orders(df_orders)
            df_orders.to_csv(orders_file, index=False)

        print("Data processing pipeline complete. Cleaned & deduplicated datasets updated.")
