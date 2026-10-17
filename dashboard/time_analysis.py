import streamlit as st
import plotly.express as px
import pandas as pd

def render_time_analysis(df_cases, df_events, df_orders, df_durations, df_metrics):
    st.title("📈 Procedural Time Analytics")
    st.markdown("Statistical breakdown of case active durations, event gap intervals, and activity relationship.")

    if df_metrics.empty:
        st.info("No metric analytics calculated.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Disposed Case Active Duration Distribution")
        valid_dur = df_metrics[df_metrics["status"] == "Disposed"]["total_duration_days"].dropna()
        if not valid_dur.empty:
            fig1 = px.histogram(valid_dur, x="total_duration_days", nbins=25,
                                labels={"total_duration_days": "Duration (Days)"},
                                color_discrete_sequence=["#3b82f6"])
            fig1.update_layout(template="plotly_dark", height=380)
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Event Gap Interval Distribution (Days)")
        if not df_durations.empty and "duration_days" in df_durations.columns:
            gaps = df_durations["duration_days"].dropna()
            fig2 = px.histogram(gaps, x="duration_days", nbins=25,
                                labels={"duration_days": "Observed Gap (Days)"},
                                color_discrete_sequence=["#10b981"])
            fig2.update_layout(template="plotly_dark", height=380)
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Observed Duration Variance across Case Types")
        if "total_duration_days" in df_metrics.columns and "case_type" in df_metrics.columns:
            df_disposed = df_metrics[df_metrics["status"] == "Disposed"].dropna(subset=["total_duration_days"])
            if not df_disposed.empty:
                fig3 = px.box(df_disposed, x="case_type", y="total_duration_days", color="case_type",
                              labels={"total_duration_days": "Duration (Days)", "case_type": "Case Type"})
                fig3.update_layout(template="plotly_dark", showlegend=False, height=380)
                st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Event Count vs. Active Case Duration")
        if "number_of_events" in df_metrics.columns and "total_duration_days" in df_metrics.columns:
            df_disp = df_metrics[df_metrics["status"] == "Disposed"].dropna(subset=["total_duration_days"])
            if not df_disp.empty:
                fig4 = px.scatter(df_disp, x="number_of_events", y="total_duration_days",
                                  color="case_type", hover_data=["case_identifier"],
                                  labels={"number_of_events": "Recorded Event Count", "total_duration_days": "Duration (Days)"})
                fig4.update_layout(template="plotly_dark", height=380)
                st.plotly_chart(fig4, use_container_width=True)
