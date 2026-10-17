import pytest
from parsers.order_parser import parse_order_search_results, extract_unique_cases
from parsers.case_parser import parse_case_details
from parsers.history_parser import parse_case_history

def test_parse_order_search_results():
    sample_html = """
    <table>
        <tr>
            <td>WPCRL/289/2026</td>
            <td>12-02-2026</td>
            <td><a href="/orders/1.pdf">View</a></td>
        </tr>
        <tr>
            <td>WPCRL/289/2026</td>
            <td>18-02-2026</td>
            <td><a href="/orders/2.pdf">View</a></td>
        </tr>
        <tr>
            <td>WPPIL/45/2026</td>
            <td>15-02-2026</td>
            <td><a href="/orders/3.pdf">View</a></td>
        </tr>
    </table>
    """
    orders = parse_order_search_results(sample_html)
    assert len(orders) == 3
    
    unique_cases = extract_unique_cases(orders)
    assert len(unique_cases) == 2
    assert "WPCRL/289/2026" in unique_cases
    assert "WPPIL/45/2026" in unique_cases

def test_parse_case_details():
    sample_html = """
    <div>CNR: UKHC010019772026</div>
    <table>
        <tr><td>Case Type</td><td>WPCRL</td></tr>
        <tr><td>Filing Number</td><td>FIL/101/2026</td></tr>
        <tr><td>Case Status</td><td>Pending</td></tr>
        <tr><td>Petitioner</td><td>Ramesh Chandra</td></tr>
        <tr><td>Respondent</td><td>State of Uttarakhand</td></tr>
    </table>
    """
    details = parse_case_details(sample_html, default_identifier="WPCRL/101/2026")
    assert details["cnr"] == "UKHC010019772026"
    assert details["status"] == "Pending"
    assert details["petitioner"] == "Ramesh Chandra"

def test_parse_case_history():
    sample_html = """
    <table>
        <tr><th>Date</th><th>Event</th><th>Purpose</th></tr>
        <tr><td>12-02-2026</td><td>Hearing</td><td>Admission</td></tr>
        <tr><td>18-02-2026</td><td>Order</td><td>Notice Returnable</td></tr>
    </table>
    """
    events = parse_case_history(sample_html, cnr="UKHC010019772026", case_identifier="WPCRL/101/2026")
    assert len(events) == 2
    assert events[0]["event_date"] == "12-02-2026"
    assert events[1]["event_date"] == "18-02-2026"
