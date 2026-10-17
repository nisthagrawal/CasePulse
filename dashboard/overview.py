import streamlit as st
import plotly.express as px
import pandas as pd
from analytics.aggregations import get_summary_kpis

def render_overview(df_cases, df_events, df_orders, df_durations, df_metrics):
    st.markdown("### 📊 Executive Overview & System KPIs")
    st.markdown("Descriptive lifecycle metrics derived from Uttarakhand High Court public records.")

    kpis = get_summary_kpis(df_cases, df_events, df_orders, df_metrics)

    # Top KPI Cards with Gradient Highlights & High Contrast Text
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Cases</div>
            <div class="metric-value">{kpis["total_cases"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-color: rgba(245, 158, 11, 0.4);">
            <div class="metric-label">Pending Cases</div>
            <div class="metric-value" style="color:#fbbf24;">{kpis["pending_cases"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-color: rgba(16, 185, 129, 0.4);">
            <div class="metric-label">Disposed Cases</div>
            <div class="metric-value" style="color:#34d399;">{kpis["disposed_cases"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Events</div>
            <div class="metric-value" style="color:#818cf8;">{kpis["total_events"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Orders</div>
            <div class="metric-value" style="color:#f43f5e;">{kpis["total_orders"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class="metric-card" style="border-color: rgba(168, 85, 247, 0.4);">
            <div class="metric-label">Median Duration</div>
            <div class="metric-value" style="color:#c084fc;">{kpis["median_observed_duration"]}d</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualizations Row 1
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Distribution by Case Type")
        if not df_cases.empty and "case_type" in df_cases.columns:
            type_counts = df_cases["case_type"].value_counts().reset_index()
            type_counts.columns = ["Case Type", "Count"]
            fig1 = px.bar(
                type_counts, x="Case Type", y="Count", color="Case Type", text="Count",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig1.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=14, family="Plus Jakarta Sans"),
                showlegend=False,
                height=380
            )
            st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown("#### Pending vs. Disposed Status Ratio")
        if not df_cases.empty and "status" in df_cases.columns:
            status_counts = df_cases["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig2 = px.pie(
                status_counts, names="Status", values="Count", hole=0.45,
                color="Status", color_discrete_map={"Pending": "#f59e0b", "Disposed": "#10b981"}
            )
            fig2.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=14, family="Plus Jakarta Sans"),
                height=380
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Visualizations Row 2
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Cases Registered by Year")
        if not df_cases.empty and "case_year" in df_cases.columns:
            year_counts = df_cases["case_year"].value_counts().sort_index().reset_index()
            year_counts.columns = ["Year", "Count"]
            fig3 = px.line(year_counts, x="Year", y="Count", markers=True, line_shape="spline")
            fig3.update_traces(line_color="#38bdf8", line_width=4, marker_size=10)
            fig3.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=14, family="Plus Jakarta Sans"),
                height=380
            )
            st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown("#### Observed Case Active Duration Distribution")
        if not df_metrics.empty and "total_duration_days" in df_metrics.columns:
            valid_d = df_metrics["total_duration_days"].dropna()
            fig4 = px.histogram(
                valid_d, x="total_duration_days", nbins=20,
                labels={"total_duration_days": "Active Duration (Days)"},
                color_discrete_sequence=["#c084fc"]
            )
            fig4.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=14, family="Plus Jakarta Sans"),
                height=380
            )
            st.plotly_chart(fig4, use_container_width=True)
