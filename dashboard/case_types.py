import streamlit as st
import plotly.express as px
import pandas as pd

def render_case_types(df_cases, df_events, df_orders, df_durations, df_metrics):
    st.title("📂 Case Type Comparative Explorer")
    st.markdown("Compare temporal dynamics and event densities across legal case categories.")

    if df_metrics.empty:
        st.info("No metrics calculated.")
        return

    # Comparative Summary Table per Case Type
    group_df = df_metrics.groupby("case_type").agg(
        total_cases=("case_identifier", "count"),
        median_duration_days=("total_duration_days", "median"),
        median_event_gap_days=("median_event_gap_days", "median"),
        avg_events_per_case=("number_of_events", "mean"),
        avg_orders_per_case=("number_of_orders", "mean")
    ).reset_index()

    group_df["median_duration_days"] = group_df["median_duration_days"].round(1)
    group_df["median_event_gap_days"] = group_df["median_event_gap_days"].round(1)
    group_df["avg_events_per_case"] = group_df["avg_events_per_case"].round(1)
    group_df["avg_orders_per_case"] = group_df["avg_orders_per_case"].round(1)

    st.subheader("Comparative Case Type Metrics")
    st.dataframe(group_df, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Median Duration by Case Type")
        fig1 = px.bar(group_df, x="case_type", y="median_duration_days", color="case_type",
                      text="median_duration_days", labels={"median_duration_days": "Median Duration (Days)", "case_type": "Case Type"})
        fig1.update_layout(template="plotly_dark", showlegend=False, height=360)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Average Events per Case by Type")
        fig2 = px.bar(group_df, x="case_type", y="avg_events_per_case", color="case_type",
                      text="avg_events_per_case", labels={"avg_events_per_case": "Avg Events", "case_type": "Case Type"})
        fig2.update_layout(template="plotly_dark", showlegend=False, height=360)
        st.plotly_chart(fig2, use_container_width=True)
