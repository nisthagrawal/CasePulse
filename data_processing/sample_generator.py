import os
import random
from datetime import datetime, timedelta
import pandas as pd

CASE_TYPES = ["WPCRL", "WPPIL", "BAIL", "FA", "SA", "ARB", "MCC"]
PETITIONERS = [
    "Ramesh Chandra Sharma",
    "M/S Himalayan Power Infrastructure Ltd",
    "Devendra Singh Bisht",
    "Sunita Devi",
    "Garhwal Vikas Mandal Association",
    "Alok Kumar Verma",
    "Kumaon Timber Traders Ltd",
    "Pankaj Joshi",
    "Meenakshi Sundaram",
    "Uttarakhand Parivahan Nigam Union"
]
RESPONDENTS = [
    "State of Uttarakhand & Others",
    "Union of India & State Pollution Control Board",
    "District Magistrate Nainital & Anr",
    "Superintendent of Police Dehradun",
    "Uttarakhand Power Corporation Ltd",
    "State of Uttarakhand through Secretary Home",
    "Vice Chancellor Kumaun University",
    "Registrar High Court of Uttarakhand"
]
JUDGES = [
    "Hon'ble Mr. Justice Manoj Kumar Tiwari",
    "Hon me Mr. Justice Sharad Kumar Sharma",
    "Hon'ble Mr. Justice Ravindra Maithani",
    "Hon me Mr. Justice Alok Kumar Verma",
    "Hon'ble Mr. Justice Rakesh Thapliyal"
]
PURPOSES = [
    "Admission / Interim Relief",
    "Notice Returnable",
    "Counter Affidavit Filing",
    "Rejoinder Affidavit",
    "Final Disposal",
    "Order Reserved",
    "Judgment Pronouncement"
]

def generate_sample_datasets(output_dir: str, sample_dir: str, num_cases: int = 40):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(sample_dir, exist_ok=True)

    cases_data = []
    events_data = []
    orders_data = []
    
    event_id_counter = 1000
    order_id_counter = 5000

    base_date = datetime(2023, 1, 1)

    for i in range(1, num_cases + 1):
        case_type = random.choice(CASE_TYPES)
        case_number = str(random.randint(10, 999))
        case_year = str(random.choice([2023, 2024, 2025, 2026]))
        case_identifier = f"{case_type}/{case_number}/{case_year}"
        cnr = f"UKHC01{random.randint(100000, 999999)}{case_year}"

        filing_days_offset = random.randint(0, 900)
        filing_dt = base_date + timedelta(days=filing_days_offset)
        reg_dt = filing_dt + timedelta(days=random.randint(1, 5))
        
        status = "Disposed" if random.random() < 0.45 else "Pending"
        
        # Generate timeline events
        num_events = random.randint(3, 9)
        current_dt = reg_dt
        case_events = []
        
        for ev_idx in range(num_events):
            gap = random.randint(4, 90)
            current_dt += timedelta(days=gap)
            
            if ev_idx == 0:
                purpose = "Admission / Interim Relief"
                ev_type = "Hearing"
            elif ev_idx == num_events - 1 and status == "Disposed":
                purpose = "Judgment Pronouncement"
                ev_type = "Order / Judgment"
            else:
                purpose = random.choice(PURPOSES)
                ev_type = "Hearing" if random.random() > 0.3 else "Order / Interim"
            
            event_id_counter += 1
            case_events.append({
                "event_id": f"EVT-{event_id_counter}",
                "cnr": cnr,
                "case_identifier": case_identifier,
                "case_number": case_number,
                "event_date": current_dt.strftime("%Y-%m-%d"),
                "event_type": ev_type,
                "purpose": purpose,
                "court_number": f"Court No. {random.randint(1, 5)}",
                "judge": random.choice(JUDGES),
                "remarks": f"Proceeding recorded on {current_dt.strftime('%d-%b-%Y')}",
                "source_url": f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/{case_identifier}"
            })

        decision_dt = current_dt.strftime("%Y-%m-%d") if status == "Disposed" else ""
        
        cases_data.append({
            "cnr": cnr,
            "case_identifier": case_identifier,
            "case_number": case_number,
            "case_type": case_type,
            "case_year": case_year,
            "filing_number": f"FIL/{random.randint(1000, 9999)}/{case_year}",
            "filing_date": filing_dt.strftime("%Y-%m-%d"),
            "registration_number": f"REG/{case_number}/{case_year}",
            "registration_date": reg_dt.strftime("%Y-%m-%d"),
            "status": status,
            "decision_date": decision_dt,
            "petitioner": random.choice(PETITIONERS),
            "respondent": random.choice(RESPONDENTS),
            "petitioner_advocate": "Adv. Ramesh Joshi & Associates",
            "respondent_advocate": "Adv. Standing Counsel Govt of Uttarakhand",
            "court_number": f"Court No. {random.randint(1, 5)}",
            "judge": random.choice(JUDGES),
            "source_url": f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/{case_identifier}"
        })

        events_data.extend(case_events)

        # Generate order records for this case
        num_orders = random.randint(1, min(4, len(case_events)))
        order_events = random.sample(case_events, num_orders)
        for ord_idx, ev in enumerate(sorted(order_events, key=lambda x: x["event_date"])):
            order_id_counter += 1
            orders_data.append({
                "order_id": f"ORD-{order_id_counter}",
                "cnr": cnr,
                "case_identifier": case_identifier,
                "case_type": case_type,
                "case_number": case_number,
                "case_year": case_year,
                "order_date": ev["event_date"],
                "order_number": str(ord_idx + 1),
                "order_url": f"https://hcservices.ecourts.gov.in/ecourtindiaHC/orders/{cnr}_{ord_idx+1}.pdf",
                "source_url": f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/{case_identifier}",
                "search_from_date": "2026-01-01",
                "search_to_date": "2026-01-31"
            })

    df_cases = pd.DataFrame(cases_data)
    df_events = pd.DataFrame(events_data)
    df_orders = pd.DataFrame(orders_data)

    # Save to sample directory and output directory
    for folder in [output_dir, sample_dir]:
        df_cases.to_csv(os.path.join(folder, "cases.csv"), index=False)
        df_events.to_csv(os.path.join(folder, "case_events.csv"), index=False)
        df_orders.to_csv(os.path.join(folder, "orders.csv"), index=False)

    print(f"Generated sample datasets: {num_cases} cases, {len(events_data)} events, {len(orders_data)} orders.")

if __name__ == "__main__":
    out_p = os.path.join(os.path.dirname(__file__), "..", "output")
    samp_p = os.path.join(os.path.dirname(__file__), "..", "data", "sample")
    generate_sample_datasets(out_p, samp_p)
