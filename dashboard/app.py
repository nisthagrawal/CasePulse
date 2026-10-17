import os
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(
    page_title="CasePulse — Interactive Court Case Lifecycle & Time Analytics",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium Global CSS System: Modern Fonts, High Contrast, Glassmorphism, Top Navigation
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
        font-size: 16px !important;
    }
    
    /* Top Header Banner */
    .app-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 50%, #030712 100%);
        padding: 24px 32px;
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.3);
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .app-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #818cf8, #38bdf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 !important;
        letter-spacing: -0.02em;
    }
    .app-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 4px;
    }

    /* Top Horizontal Navigation Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #1e293b;
        padding: 8px 12px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 28px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre;
        border-radius: 10px;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0px 24px !important;
        border: none !important;
        background-color: transparent !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.39) !important;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 24px 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        text-align: center;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #6366f1;
    }
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #38bdf8;
        margin: 10px 0;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.95rem !important;
        color: #cbd5e1;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* Expanders & Form Components */
    .stExpander {
        background-color: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    /* Table Styling Overrides */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Input & Select Box styling */
    .stSelectbox label, .stTextInput label {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #e2e8f0 !important;
        margin-bottom: 8px !important;
    }

    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
        transition: transform 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        transform: scale(1.03) !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    output_dir = os.path.join(base_dir, "output")
    sample_dir = os.path.join(base_dir, "data", "sample")
    
    folder = output_dir if os.path.exists(os.path.join(output_dir, "cases.csv")) else sample_dir

    def read_csv_safe(name):
        p = os.path.join(folder, name)
        if os.path.exists(p):
            return pd.read_csv(p)
        return pd.DataFrame()

    df_cases = read_csv_safe("cases.csv")
    df_events = read_csv_safe("case_events.csv")
    df_orders = read_csv_safe("orders.csv")
    df_durations = read_csv_safe("event_durations.csv")
    df_metrics = read_csv_safe("case_metrics.csv")

    return df_cases, df_events, df_orders, df_durations, df_metrics

def main():
    # Top Header Banner
    st.markdown("""
    <div class="app-header">
        <div>
            <h1 class="app-title">⚖️ CASEPULSE</h1>
            <div class="app-subtitle">Uttarakhand High Court — Interactive Court Case Lifecycle & Temporal Analytics</div>
        </div>
        <div>
            <span style="background: rgba(99, 102, 241, 0.2); border: 1px solid #818cf8; color: #a5b4fc; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">
                🟢 System Active
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df_cases, df_events, df_orders, df_durations, df_metrics = load_data()

    if df_cases.empty:
        st.warning("⚠️ No dataset loaded. Generating sample dataset...")
        from data_processing.sample_generator import generate_sample_datasets
        from analytics.duration_engine import calculate_event_durations
        from analytics.case_metrics import generate_case_metrics
        
        base_dir = os.path.join(os.path.dirname(__file__), "..")
        output_dir = os.path.join(base_dir, "output")
        sample_dir = os.path.join(base_dir, "data", "sample")
        generate_sample_datasets(output_dir, sample_dir, num_cases=40)
        
        df_cases, df_events, df_orders, df_durations, df_metrics = load_data()

    # Top Navigation Tabs (Replaces Sidebar)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 1. Executive Overview",
        "🔍 2. Case Explorer & Timeline",
        "📈 3. Time Analytics",
        "📂 4. Case Type Comparison",
        "💾 5. Data Explorer & CSV Export"
    ])

    with tab1:
        from dashboard.overview import render_overview
        render_overview(df_cases, df_events, df_orders, df_durations, df_metrics)

    with tab2:
        from dashboard.case_explorer import render_case_explorer
        render_case_explorer(df_cases, df_events, df_orders, df_durations, df_metrics)

    with tab3:
        from dashboard.time_analysis import render_time_analysis
        render_time_analysis(df_cases, df_events, df_orders, df_durations, df_metrics)

    with tab4:
        from dashboard.case_types import render_case_types
        render_case_types(df_cases, df_events, df_orders, df_durations, df_metrics)

    with tab5:
        from dashboard.data_explorer import render_data_explorer
        render_data_explorer(df_cases, df_events, df_orders, df_durations, df_metrics)

if __name__ == "__main__":
    main()
