from bs4 import BeautifulSoup
import re
from typing import List, Dict

def parse_order_search_results(html_content: str, search_from_date: str = "", search_to_date: str = "") -> List[Dict]:
    """
    Dynamically extracts orders and discovers unique cases from Order-Date search html response.
    Maps columns dynamically based on header text inspection rather than static column indices.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    orders = []

    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue
            
        header_row = rows[0]
        headers = [h.get_text(strip=True).lower() for h in header_row.find_all(["th", "td"])]
        
        # Determine column mappings dynamically
        case_col_idx = -1
        date_col_idx = -1
        order_no_col_idx = -1
        
        for idx, h_text in enumerate(headers):
            if "case" in h_text or "number" in h_text or "petition" in h_text:
                if case_col_idx == -1:
                    case_col_idx = idx
            if "date" in h_text or "order date" in h_text:
                if date_col_idx == -1:
                    date_col_idx = idx
            if "order no" in h_text or "order number" in h_text or "sr" in h_text:
                if order_no_col_idx == -1:
                    order_no_col_idx = idx

        for row in rows[1:]:
            cols = row.find_all(["td", "th"])
            if len(cols) < 2:
                continue

            row_text = " ".join([c.get_text(strip=True) for c in cols])
            
            # Dynamic regex extraction for case identifier
            case_match = re.search(r'([A-Za-z]+)\s*[/|-]\s*(\d+)\s*[/|-]\s*(\d{4})', row_text)
            date_match = re.search(r'(\d{2}[-/.]\d{2}[-/.]\d{4})', row_text)
            
            if case_match:
                case_type = case_match.group(1).upper()
                case_number = case_match.group(2)
                case_year = case_match.group(3)
                case_identifier = f"{case_type}/{case_number}/{case_year}"
                
                order_date = date_match.group(1) if date_match else ""
                
                link = row.find("a", href=True)
                order_url = link["href"] if link else ""
                
                orders.append({
                    "case_identifier": case_identifier,
                    "case_type": case_type,
                    "case_number": case_number,
                    "case_year": case_year,
                    "order_date": order_date,
                    "order_number": str(len(orders) + 1),
                    "order_url": order_url,
                    "source_url": "",
                    "search_from_date": search_from_date,
                    "search_to_date": search_to_date
                })

    return orders

def extract_unique_cases(orders: List[Dict]) -> List[str]:
    unique_cases = sorted(list(set(ord["case_identifier"] for ord in orders if "case_identifier" in ord)))
    return unique_cases
