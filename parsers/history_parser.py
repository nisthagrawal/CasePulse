from bs4 import BeautifulSoup
import re
from typing import List, Dict

def parse_case_history(html_content: str, cnr: str = "", case_identifier: str = "") -> List[Dict]:
    """
    Parses case history events timeline table from eCourts case history section.
    Extracts event date, event type, purpose, judge, court number, remarks.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    events = []
    
    # Locate History table (often contains headers like 'Business Date', 'Hearing Date', 'Purpose of Hearing', 'Judge')
    tables = soup.find_all("table")
    event_counter = 1
    
    for table in tables:
        header_text = table.get_text().lower()
        if "date" in header_text or "purpose" in header_text or "hearing" in header_text:
            rows = table.find_all("tr")
            for row in rows:
                cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
                if len(cols) < 2:
                    continue
                
                # Check for date in columns
                date_found = ""
                for col in cols:
                    match = re.search(r'(\d{2}[-/.]\d{2}[-/.]\d{4})', col)
                    if match:
                        date_found = match.group(1)
                        break
                
                if date_found:
                    event_id = f"EVT-{cnr or case_identifier}-{event_counter}"
                    event_counter += 1
                    
                    event_type = cols[1] if len(cols) > 1 else "Hearing"
                    purpose = cols[2] if len(cols) > 2 else "Proceeding"
                    judge = cols[3] if len(cols) > 3 else ""
                    remarks = cols[4] if len(cols) > 4 else ""
                    
                    events.append({
                        "event_id": event_id,
                        "cnr": cnr,
                        "case_identifier": case_identifier,
                        "case_number": case_identifier.split("/")[1] if "/" in case_identifier else "",
                        "event_date": date_found,
                        "event_type": event_type,
                        "purpose": purpose,
                        "court_number": "",
                        "judge": judge,
                        "remarks": remarks,
                        "source_url": ""
                    })

    return events
