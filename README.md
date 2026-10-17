# CasePulse: An Interactive Court Case Lifecycle and Procedural Time Analytics System

CasePulse transforms publicly accessible Uttarakhand High Court case, order, and history records into structured temporal datasets to explore case lifecycle patterns, event intervals, case activity, and observed duration through interactive visualizations.

## Core Features
- **Data Acquisition**: Playwright crawler supporting bulk Order-Date search (`orders-by-date`) and individual case lookup (`interactive`).
- **Data Engineering**: Automated schema validation, date normalization (`YYYY-MM-DD`), deduplication, and raw HTML preservation.
- **Temporal Analytics Engine**: Computes consecutive event gap intervals (`event_durations.csv`) and case-level metrics (`case_metrics.csv`).
- **Interactive Dashboard**: Modern Streamlit + Plotly application featuring 5 specialized analytical pages, including the signature **Case Lifecycle Timeline**.
- **Sample Data Generator**: Pre-populate realistic synthetic datasets out-of-the-box for instant exploration.

## Installation & Setup

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. **Generate Sample Data**:
```bash
python main.py generate-sample
```

3. **Process Pipeline Data**:
```bash
python main.py process-data
```

4. **Launch Streamlit Dashboard**:
```bash
python main.py run-dashboard
```
or
```bash
streamlit run dashboard/app.py
```

5. **Run Bulk Crawler (eCourts Order-Date Search)**:
```bash
python main.py orders-by-date --from 01-01-2026 --to 31-01-2026
```

## Software Architecture

```
CasePulse/
├── main.py                  # Master CLI controller
├── crawler/                # Playwright automation & state tracking
├── parsers/                # BeautifulSoup HTML extraction modules
├── data_processing/        # Normalization, cleaning, & deduplication
├── analytics/              # Temporal engine & duration calculation
├── dashboard/              # Multi-page Streamlit application
├── tests/                  # Pytest test suite
├── data/                   # Raw, processed, and sample datasets
└── output/                 # Final analytical CSV datasets
```
