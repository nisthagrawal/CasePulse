import os
import random
from datetime import datetime, timedelta
import pandas as pd

CASE_TYPES = [
    "WPCRL",    # Writ Petition Criminal
    "WPPIL",    # Writ Petition Public Interest Litigation
    "WPMS",     # Writ Petition Miscellaneous Single
    "BAIL",     # First Bail Application
    "ABAIL",    # Anticipatory Bail Application
    "C482",     # Application u/s 482 Cr.P.C.
    "CRLREV",   # Criminal Revision
    "FA",       # First Appeal
    "SA",       # Second Appeal
    "ARB",      # Arbitration Application
    "CONT",     # Contempt Petition
    "MCC"       # Miscellaneous Civil Case
]

PETITIONERS = [
    "Ramesh Chandra Sharma",
    "M/S Himalayan Power Infrastructure Ltd.",
    "Devendra Singh Bisht",
    "Sunita Devi",
    "Garhwal Vikas Mandal Association",
    "Alok Kumar Verma",
    "Kumaon Timber Traders & Wood Products Ltd.",
    "Pankaj Joshi & Anr.",
    "Meenakshi Sundaram",
    "Uttarakhand Parivahan Nigam Union",
    "Doon Valley Environmental Protection Samiti",
    "Dr. Rajendra Prasad Nautiyal",
    "Smt. Kamla Bhatt",
    "Mahesh Chandra Pant",
    "Virendra Singh Rawat",
    "M/S Shivalik Construction & Earthmovers",
    "Haridwar Ganga Ghat Cleanliness Trust",
    "Kedar Valley Hospitality Association",
    "Anil Kumar Negi",
    "Smt. Geeta Devi Bisht"
]

RESPONDENTS = [
    "State of Uttarakhand through Principal Secretary (Home)",
    "State of Uttarakhand through Secretary (Forest & Environment)",
    "Union of India & State Pollution Control Board",
    "District Magistrate Nainital & Senior Superintendent of Police",
    "District Magistrate Dehradun & Anr.",
    "Uttarakhand Power Corporation Ltd. (UPCL) through MD",
    "State of Uttarakhand through Secretary (Revenue)",
    "Vice Chancellor Kumaun University, Nainital",
    "Public Works Department (PWD) Uttarakhand",
    "Uttarakhand Transport Corporation",
    "Registrar General, High Court of Uttarakhand",
    "Nagar Palika Parishad Mussoorie",
    "Superintendent of Police Haridwar",
    "Uttarakhand Jal Sansthan through Chief Engineer"
]

JUDGES = [
    "Hon'ble The Chief Justice Ritu Bahri",
    "Hon'ble Mr. Justice Manoj Kumar Tiwari",
    "Hon'ble Mr. Justice Ravindra Maithani",
    "Hon'ble Mr. Justice Alok Kumar Verma",
    "Hon'ble Mr. Justice Rakesh Thapliyal",
    "Hon'ble Mr. Justice Pankaj Purohit",
    "Hon'ble Mr. Justice Vivek Bharti Sharma"
]

PETITIONER_ADVOCATES = [
    "Adv. Arvind Vashistha (Senior Advocate)",
    "Adv. Siddhartha Singh",
    "Adv. D.S. Patni (Senior Advocate)",
    "Adv. B.S. Adhikari",
    "Adv. Meenakshi Sharma",
    "Adv. Vikas Bahuguna",
    "Adv. Deepa Arya",
    "Adv. Amit Kapri",
    "Adv. K.S. Rautela",
    "Adv. Saurabh Kumar Pandey"
]

RESPONDENT_ADVOCATES = [
    "Adv. C.S. Rawat, Chief Standing Counsel",
    "Adv. J.S. Virk, Deputy Advocate General",
    "Adv. Pradeep Joshi, Additional Chief Standing Counsel",
    "Adv. Lalit Sharma, Standing Counsel for Union of India",
    "Adv. Dharmendra Barthwal, Counsel for UPCL",
    "Adv. T.A. Khan (Senior Advocate)",
    "Adv. Devendra Singh Bohra",
    "Adv. Sandeep Kothari"
]

STAGES_PIPELINE = [
    ("Admission / Interim Relief", "Hearing", 7, 25),
    ("Notice Issued to Respondents", "Hearing", 14, 35),
    ("Counter Affidavit by State / Respondent", "Hearing", 20, 60),
    ("Rejoinder Affidavit Filing", "Hearing", 15, 45),
    ("Hearing on Interlocutory Application", "Order / Interim", 10, 40),
    ("Lower Court Records Summoned", "Hearing", 25, 75),
    ("Final Arguments Commenced", "Hearing", 14, 50),
    ("Order Reserved", "Hearing", 7, 21),
    ("Judgment Pronouncement", "Order / Judgment", 5, 20)
]

def generate_sample_datasets(output_dir: str, sample_dir: str, num_cases: int = 500):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(sample_dir, exist_ok=True)

    cases_data = []
    events_data = []
    orders_data = []
    
    event_id_counter = 10000
    order_id_counter = 50000

    base_date = datetime(2022, 1, 1)

    # Set seed for reproducible yet realistic statistical distribution
    random.seed(42)

    for i in range(1, num_cases + 1):
        case_type = random.choices(
            CASE_TYPES,
            weights=[18, 8, 16, 20, 10, 8, 5, 4, 3, 2, 3, 3],
            k=1
        )[0]
        case_number = str(random.randint(10, 9999))
        case_year = str(random.choices([2022, 2023, 2024, 2025, 2026], weights=[15, 25, 30, 20, 10], k=1)[0])
        case_identifier = f"{case_type}/{case_number}/{case_year}"
        cnr = f"UKHC01{random.randint(100000, 999999)}{case_year}"

        # Filing date between 2022 and early 2026
        max_filing_days = min(1400, (datetime(2026, 2, 1) - base_date).days)
        filing_days_offset = random.randint(0, max_filing_days)
        filing_dt = base_date + timedelta(days=filing_days_offset)
        reg_dt = filing_dt + timedelta(days=random.randint(1, 6))

        # Disposal probability is higher for older cases
        filing_year = int(case_year)
        if filing_year <= 2023:
            disposal_prob = 0.78
        elif filing_year == 2024:
            disposal_prob = 0.55
        elif filing_year == 2025:
            disposal_prob = 0.35
        else:
            disposal_prob = 0.15

        is_disposed = random.random() < disposal_prob
        status = "Disposed" if is_disposed else "Pending"

        # Determine number of procedural stages
        if is_disposed:
            num_events = random.randint(5, len(STAGES_PIPELINE))
            selected_stages = STAGES_PIPELINE[:num_events - 1] + [STAGES_PIPELINE[-1]]
        else:
            num_events = random.randint(2, len(STAGES_PIPELINE) - 2)
            selected_stages = STAGES_PIPELINE[:num_events]

        current_dt = reg_dt
        case_events = []
        assigned_judge = random.choice(JUDGES)
        assigned_court = f"Court No. {random.randint(1, 7)}"
        pet_adv = random.choice(PETITIONER_ADVOCATES)
        resp_adv = random.choice(RESPONDENT_ADVOCATES)

        for ev_idx, (stage_name, default_type, min_gap, max_gap) in enumerate(selected_stages):
            # Bail cases move faster
            if "BAIL" in case_type:
                gap = random.randint(max(3, min_gap // 2), max(7, max_gap // 2))
            else:
                gap = random.randint(min_gap, max_gap)

            current_dt += timedelta(days=gap)

            # Prevent future dates past today
            if current_dt > datetime(2026, 10, 17):
                current_dt = datetime(2026, 10, 15) - timedelta(days=random.randint(1, 10))

            event_id_counter += 1
            case_events.append({
                "event_id": f"EVT-{event_id_counter}",
                "cnr": cnr,
                "case_identifier": case_identifier,
                "case_number": case_number,
                "event_date": current_dt.strftime("%Y-%m-%d"),
                "event_type": default_type,
                "purpose": stage_name,
                "court_number": assigned_court,
                "judge": assigned_judge,
                "remarks": f"Proceeding for {stage_name} conducted on {current_dt.strftime('%d-%b-%Y')}",
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
            "petitioner_advocate": pet_adv,
            "respondent_advocate": resp_adv,
            "court_number": assigned_court,
            "judge": assigned_judge,
            "source_url": f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/{case_identifier}"
        })

        events_data.extend(case_events)

        # Generate orders: 1 to 4 orders per case corresponding to hearings
        num_orders = random.randint(1, min(5, len(case_events)))
        order_events = sorted(random.sample(case_events, num_orders), key=lambda x: x["event_date"])

        for ord_idx, ev in enumerate(order_events):
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

    for folder in [output_dir, sample_dir]:
        df_cases.to_csv(os.path.join(folder, "cases.csv"), index=False)
        df_events.to_csv(os.path.join(folder, "case_events.csv"), index=False)
        df_orders.to_csv(os.path.join(folder, "orders.csv"), index=False)

    print(f"[SUCCESS] Generated high-fidelity dataset: {num_cases} cases, {len(events_data)} events, {len(orders_data)} orders.")
    return df_cases, df_events, df_orders

if __name__ == "__main__":
    out_p = os.path.join(os.path.dirname(__file__), "..", "output")
    samp_p = os.path.join(os.path.dirname(__file__), "..", "data", "sample")
    generate_sample_datasets(out_p, samp_p, num_cases=500)
