import streamlit as st
import pandas as pd

def render_data_explorer(df_cases, df_events, df_orders, df_durations, df_metrics):
    st.markdown("### 💾 Raw & Derived Data Explorer")
    st.markdown("Inspect underlying structured datasets and export CSV records for auditing and reproducible research.")

    sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs([
        "📁 Cases Dataset",
        "⚡ Case Events",
        "📄 Orders Dataset",
        "⏱️ Event Durations",
        "📊 Case Metrics"
    ])

    with sub_tab1:
        st.markdown("#### `cases.csv` — Case-Level Primary Records")
        if not df_cases.empty:
            st.dataframe(df_cases, use_container_width=True, height=450)
            st.markdown("<br>", unsafe_allow_html=True)
            csv = df_cases.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download cases.csv", csv, "cases.csv", "text/csv")
        else:
            st.info("No cases dataset loaded.")

    with sub_tab2:
        st.markdown("#### `case_events.csv` — Sequential Event Records")
        if not df_events.empty:
            st.dataframe(df_events, use_container_width=True, height=450)
            st.markdown("<br>", unsafe_allow_html=True)
            csv = df_events.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download case_events.csv", csv, "case_events.csv", "text/csv")
        else:
            st.info("No events dataset loaded.")

    with sub_tab3:
        st.markdown("#### `orders.csv` — Judicial Order Records")
        if not df_orders.empty:
            st.dataframe(df_orders, use_container_width=True, height=450)
            st.markdown("<br>", unsafe_allow_html=True)
            csv = df_orders.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download orders.csv", csv, "orders.csv", "text/csv")
        else:
            st.info("No orders dataset loaded.")

    with sub_tab4:
        st.markdown("#### `event_durations.csv` — Consecutive Event Interval Gaps")
        if not df_durations.empty:
            st.dataframe(df_durations, use_container_width=True, height=450)
            st.markdown("<br>", unsafe_allow_html=True)
            csv = df_durations.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download event_durations.csv", csv, "event_durations.csv", "text/csv")
        else:
            st.info("No durations dataset loaded.")

    with sub_tab5:
        st.markdown("#### `case_metrics.csv` — Primary Analytical Dataset")
        if not df_metrics.empty:
            st.dataframe(df_metrics, use_container_width=True, height=450)
            st.markdown("<br>", unsafe_allow_html=True)
            csv = df_metrics.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download case_metrics.csv", csv, "case_metrics.csv", "text/csv")
        else:
            st.info("No metrics dataset loaded.")
