import os
import logging
from typing import Dict, Tuple, List
from playwright.async_api import Page
from crawler.browser import ECOURTS_UTTARAKHAND_URL
from parsers.case_parser import parse_case_details
from parsers.history_parser import parse_case_history

logger = logging.getLogger(__name__)

async def search_individual_case(page: Page, case_type: str, case_number: str, case_year: str, raw_dir: str = "data/raw/case_details") -> Tuple[Dict, List[Dict]]:
    """
    Mode 2 — Individual Case Search.
    Navigates to eCourts case search, searches for case by type, number, year.
    """
    os.makedirs(raw_dir, exist_ok=True)
    logger.info(f"Navigating to eCourts Uttarakhand main page: {ECOURTS_UTTARAKHAND_URL}")
    
    await page.goto(ECOURTS_UTTARAKHAND_URL, wait_until="domcontentloaded")
    
    print("\n" + "="*70)
    print(f"MODE 2: INDIVIDUAL CASE SEARCH ({case_type}/{case_number}/{case_year})")
    print("Please complete the visible CAPTCHA on page and submit to view case details.")
    print("="*70 + "\n")
    
    try:
        await page.wait_for_selector("table", timeout=60000)
    except Exception:
        pass

    content = await page.content()
    case_identifier = f"{case_type}/{case_number}/{case_year}"
    
    raw_path = os.path.join(raw_dir, f"case_{case_type}_{case_number}_{case_year}.html")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(content)

    case_details = parse_case_details(content, default_identifier=case_identifier)
    case_events = parse_case_history(content, cnr=case_details.get("cnr", ""), case_identifier=case_identifier)

    return case_details, case_events
