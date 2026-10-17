from bs4 import BeautifulSoup
import re
from typing import Dict

def parse_case_details(html_content: str, default_identifier: str = "") -> Dict:
    """
    Parses case details HTML from eCourts case view page.
    Extracts CNR, Filing No, Registration No, Status, Advocates, Judge, Petitioner, Respondent.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    data = {
        "cnr": "",
        "case_identifier": default_identifier,
        "case_number": "",
        "case_type": "",
        "case_year": "",
        "filing_number": "",
        "filing_date": "",
        "registration_number": "",
        "registration_date": "",
        "status": "Pending",
        "decision_date": "",
        "petitioner": "",
        "respondent": "",
        "petitioner_advocate": "",
        "respondent_advocate": "",
        "court_number": "",
        "judge": "",
        "source_url": ""
    }

    # Extract CNR Number (usually matching UKHC...)
    cnr_match = re.search(r'UKHC[0-9A-Z]{12}', html_content)
    if cnr_match:
        data["cnr"] = cnr_match.group(0)

    # Extract Key-Value tables
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cols) >= 2:
                label = cols[0].lower()
                val = cols[1]
                
                if "case type" in label:
                    data["case_type"] = val
                elif "filing number" in label:
                    data["filing_number"] = val
                elif "filing date" in label:
                    data["filing_date"] = val
                elif "registration number" in label:
                    data["registration_number"] = val
                elif "registration date" in label:
                    data["registration_date"] = val
                elif "case status" in label or "status" in label:
                    if "disposed" in val.lower() or "decided" in val.lower():
                        data["status"] = "Disposed"
                    else:
                        data["status"] = "Pending"
                elif "decision date" in label:
                    data["decision_date"] = val
                elif "petitioner" in label and not data["petitioner"]:
                    data["petitioner"] = val
                elif "respondent" in label and not data["respondent"]:
                    data["respondent"] = val
                elif "petitioner advocate" in label:
                    data["petitioner_advocate"] = val
                elif "respondent advocate" in label:
                    data["respondent_advocate"] = val
                elif "judge" in label:
                    data["judge"] = val
                elif "court number" in label or "court no" in label:
                    data["court_number"] = val

    if not data["case_identifier"] and data["case_type"] and data["case_number"] and data["case_year"]:
        data["case_identifier"] = f"{data['case_type']}/{data['case_number']}/{data['case_year']}"

    return data
