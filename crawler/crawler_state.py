import os
import json
import csv
from datetime import datetime

class CrawlerState:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.state_file = os.path.join(self.output_dir, "crawl_state.json")
        self.log_file = os.path.join(self.output_dir, "crawl_log.csv")

        self.state = self.load_state()
        self._init_log_file()

    def load_state(self) -> dict:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "date_range": {"from_date": "", "to_date": ""},
            "discovered_cases": [],
            "processed_cases": [],
            "failed_cases": [],
            "last_updated": datetime.now().isoformat()
        }

    def save_state(self):
        self.state["last_updated"] = datetime.now().isoformat()
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def _init_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "stage", "case_identifier", "url", "status", "error_type", "message"
                ])

    def log(self, stage: str, case_identifier: str, url: str, status: str, error_type: str = "", message: str = ""):
        timestamp = datetime.now().isoformat()
        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, stage, case_identifier, url, status, error_type, message])

    def add_discovered_case(self, case_id: str):
        if case_id not in self.state["discovered_cases"]:
            self.state["discovered_cases"].append(case_id)
            self.save_state()

    def mark_processed(self, case_id: str):
        if case_id not in self.state["processed_cases"]:
            self.state["processed_cases"].append(case_id)
            if case_id in self.state["failed_cases"]:
                self.state["failed_cases"].remove(case_id)
            self.save_state()

    def mark_failed(self, case_id: str, error_type: str = "", message: str = ""):
        if case_id not in self.state["failed_cases"]:
            self.state["failed_cases"].append(case_id)
            self.save_state()
        self.log("EXTRACTION", case_id, "", "FAILED", error_type, message)
