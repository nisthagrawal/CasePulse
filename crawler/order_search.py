import os
import asyncio
import logging
from datetime import datetime
from typing import Tuple, List, Dict
from playwright.async_api import Page
from crawler.browser import ECOURTS_ORDER_DATE_URL
from parsers.order_parser import parse_order_search_results, extract_unique_cases

logger = logging.getLogger(__name__)

async def search_orders_by_date(page: Page, from_date: str, to_date: str, raw_dir: str = "data/raw/orders") -> Tuple[List[Dict], List[str]]:
    """
    Performs Order-Date search on Uttarakhand eCourts.
    Fills date parameters, pauses for human CAPTCHA input if required, and extracts returned orders & unique case IDs.
    """
    os.makedirs(raw_dir, exist_ok=True)
    logger.info(f"Navigating to Order Date Search: {ECOURTS_ORDER_DATE_URL}")
    
    try:
        await page.goto(ECOURTS_ORDER_DATE_URL, wait_until="networkidle", timeout=30000)
    except Exception as e:
        logger.warning(f"Initial navigation warning: {e}. Retrying with domcontentloaded...")
        await page.goto(ECOURTS_ORDER_DATE_URL, wait_until="domcontentloaded")

    # Fill date range inputs if selectors exist
    try:
        if await page.locator("#from_date").count() > 0:
            await page.fill("#from_date", from_date)
        if await page.locator("#to_date").count() > 0:
            await page.fill("#to_date", to_date)
    except Exception as e:
        logger.warning(f"Could not fill date selectors automatically: {e}")

    print("\n" + "="*70)
    print("ACTION REQUIRED: CAPTCHA / Form Verification")
    print(f"Please inspect the browser window for date range ({from_date} to {to_date}),")
    print("complete the visible CAPTCHA, and submit the official eCourts form.")
    print("="*70 + "\n")

    # In interactive/automated context, wait for table or results to appear
    try:
        # Give user time or wait for result table selector
        await page.wait_for_selector("table", timeout=60000)
    except Exception:
        logger.info("Timeout waiting for table selector. Reading page content directly...")

    content = await page.content()
    
    # Save raw HTML for reproducibility
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = os.path.join(raw_dir, f"order_search_{from_date}_{to_date}_{timestamp}.html")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(content)

    orders = parse_order_search_results(content, search_from_date=from_date, search_to_date=to_date)
    unique_cases = extract_unique_cases(orders)
    
    logger.info(f"Extracted {len(orders)} orders for {len(unique_cases)} unique cases.")
    return orders, unique_cases
