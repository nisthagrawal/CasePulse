import os
import sys
import argparse
import asyncio
import subprocess
import pandas as pd

# Path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from data_processing.sample_generator import generate_sample_datasets
from data_processing.cleaner import clean_cases_dataframe, clean_events_dataframe, clean_orders_dataframe
from data_processing.deduplicator import deduplicate_cases, deduplicate_events, deduplicate_orders
from analytics.duration_engine import calculate_event_durations
from analytics.case_metrics import generate_case_metrics

def cmd_generate_sample(args):
    output_dir = os.path.join(BASE_DIR, "output")
    sample_dir = os.path.join(BASE_DIR, "data", "sample")
    print(f"Generating synthetic sample datasets into {sample_dir} and {output_dir}...")
    generate_sample_datasets(output_dir, sample_dir, num_cases=args.num_cases)
    print("Running analytics pipeline on generated sample data...")
    cmd_process_data(args)

def cmd_process_data(args):
    output_dir = os.path.join(BASE_DIR, "output")
    
    cases_p = os.path.join(output_dir, "cases.csv")
    events_p = os.path.join(output_dir, "case_events.csv")
    orders_p = os.path.join(output_dir, "orders.csv")
    durations_p = os.path.join(output_dir, "event_durations.csv")
    metrics_p = os.path.join(output_dir, "case_metrics.csv")

    if not os.path.exists(cases_p):
        print(f"Error: {cases_p} not found. Run `python main.py generate-sample` first.")
        return

    df_cases = pd.read_csv(cases_p)
    df_events = pd.read_csv(events_p) if os.path.exists(events_p) else pd.DataFrame()
    df_orders = pd.read_csv(orders_p) if os.path.exists(orders_p) else pd.DataFrame()

    print("Cleaning & deduplicating raw datasets...")
    df_cases = deduplicate_cases(clean_cases_dataframe(df_cases))
    df_events = deduplicate_events(clean_events_dataframe(df_events))
    df_orders = deduplicate_orders(clean_orders_dataframe(df_orders))

    print("Computing consecutive event gap durations (event_durations.csv)...")
    df_durations = calculate_event_durations(df_events)

    print("Calculating aggregated case metrics (case_metrics.csv)...")
    df_metrics = generate_case_metrics(df_cases, df_events, df_orders, df_durations)

    df_cases.to_csv(cases_p, index=False)
    df_events.to_csv(events_p, index=False)
    df_orders.to_csv(orders_p, index=False)
    df_durations.to_csv(durations_p, index=False)
    df_metrics.to_csv(metrics_p, index=False)

    print("✅ Data engineering & analytics pipeline successfully completed.")

def cmd_run_dashboard(args):
    app_path = os.path.join(BASE_DIR, "dashboard", "app.py")
    print(f"Launching Streamlit CasePulse dashboard from {app_path}...")
    cmd = [sys.executable, "-m", "streamlit", "run", app_path]
    subprocess.run(cmd)

def cmd_orders_by_date(args):
    from crawler.browser import get_browser_page
    from crawler.order_search import search_orders_by_date
    from crawler.crawler_state import CrawlerState

    output_dir = os.path.join(BASE_DIR, "output")
    state = CrawlerState(output_dir)
    from_date = args.from_date or "01-01-2026"
    to_date = args.to_date or "31-01-2026"

    async def run():
        async with get_browser_page(headless=args.headless) as page:
            orders, unique_cases = await search_orders_by_date(page, from_date, to_date)
            for c in unique_cases:
                state.add_discovered_case(c)
            print(f"Discovered {len(unique_cases)} unique cases from order date search.")

    asyncio.run(run())

def cmd_interactive(args):
    from crawler.browser import get_browser_page
    from crawler.case_search import search_individual_case

    case_type = args.type or "WPCRL"
    case_num = args.number or "101"
    case_year = args.year or "2026"

    async def run():
        async with get_browser_page(headless=args.headless) as page:
            details, events = await search_individual_case(page, case_type, case_num, case_year)
            print(f"Case Details: {details}")
            print(f"Recorded Events: {len(events)}")

    asyncio.run(run())

def main():
    parser = argparse.ArgumentParser(
        description="CasePulse — Court Case Lifecycle and Procedural Time Analytics System"
    )
    subparsers = parser.add_subparsers(dest="command", help="System command mode")

    # generate-sample
    p_samp = subparsers.add_parser("generate-sample", help="Generate synthetic sample dataset")
    p_samp.add_argument("--num-cases", type=int, default=40, help="Number of sample cases to generate")

    # process-data
    subparsers.add_parser("process-data", help="Execute cleaning, deduplication, and analytics calculations")

    # run-dashboard
    subparsers.add_parser("run-dashboard", help="Launch interactive Streamlit dashboard")

    # orders-by-date
    p_ord = subparsers.add_parser("orders-by-date", help="Mode 1: Bulk Order-Date Search")
    p_ord.add_argument("--from-date", type=str, default="01-01-2026", help="From date (DD-MM-YYYY)")
    p_ord.add_argument("--to-date", type=str, default="31-01-2026", help="To date (DD-MM-YYYY)")
    p_ord.add_argument("--headless", action="store_true", help="Run browser in headless mode")

    # interactive
    p_ind = subparsers.add_parser("interactive", help="Mode 2: Individual Case Search")
    p_ind.add_argument("--type", type=str, default="WPCRL", help="Case Type")
    p_ind.add_argument("--number", type=str, default="101", help="Case Number")
    p_ind.add_argument("--year", type=str, default="2026", help="Case Year")
    p_ind.add_argument("--headless", action="store_true", help="Run browser in headless mode")

    args = parser.parse_args()

    if args.command == "generate-sample":
        cmd_generate_sample(args)
    elif args.command == "process-data":
        cmd_process_data(args)
    elif args.command == "run-dashboard":
        cmd_run_dashboard(args)
    elif args.command == "orders-by-date":
        cmd_orders_by_date(args)
    elif args.command == "interactive":
        cmd_interactive(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
