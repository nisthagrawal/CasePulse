import os
import logging
from typing import Dict, List, Tuple
from playwright.async_api import Page
from parsers.case_parser import parse_case_details
from parsers.history_parser import parse_case_history

logger = logging.getLogger(__name__)

async def fetch_case_details_and_history(page: Page, case_identifier: str, raw_dir: str = "data/raw/case_history") -> Tuple[Dict, List[Dict]]:
    """
    Fetches full case details and history timeline given a discovered case identifier.
    """
    os.makedirs(raw_dir, exist_ok=True)
    logger.info(f"Fetching case history for discovered case: {case_identifier}")
    
    # In live eCourts, this navigates to case view endpoint
    content = await page.content()
    
    clean_id = case_identifier.replace("/", "_")
    raw_path = os.path.join(raw_dir, f"history_{clean_id}.html")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(content)

    case_details = parse_case_details(content, default_identifier=case_identifier)
    case_events = parse_case_history(content, cnr=case_details.get("cnr", ""), case_identifier=case_identifier)

    return case_details, case_events
