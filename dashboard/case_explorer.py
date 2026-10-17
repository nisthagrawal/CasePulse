import streamlit as st
import pandas as pd
from datetime import datetime

def render_case_explorer(df_cases, df_events, df_orders, df_durations, df_metrics):
    st.markdown("### 🔍 Case Explorer & Lifecycle Timeline")
    st.markdown("Select a court case to inspect metadata, legal parties, and the step-by-step procedural event timeline.")

    if df_cases.empty:
        st.info("No case records available.")
        return

    # Case Selection Header
    col_sel1, col_sel2 = st.columns([2, 2])

    with col_sel1:
        case_options = sorted(df_cases["case_identifier"].dropna().unique().tolist())
        selected_case_id = st.selectbox("📌 Select Case Identifier:", case_options, index=0)

    with col_sel2:
        cnr_search = st.text_input("🔎 Or Search by CNR Identifier:", placeholder="e.g. UKHC010019772026")
        if cnr_search.strip():
            matched = df_cases[df_cases["cnr"].astype(str).str.contains(cnr_search.strip(), case=False, na=False)]
            if not matched.empty:
                selected_case_id = matched.iloc[0]["case_identifier"]
                st.success(f"Found case match: {selected_case_id}")

    case_row = df_cases[df_cases["case_identifier"] == selected_case_id].iloc[0]

    # Key Case Metadata Highlights Cards
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        st.markdown(f"""
        <div style="background:#1e293b; border-radius:12px; padding:16px; border:1px solid rgba(255,255,255,0.1); text-align:center;">
            <div style="color:#94a3b8; font-size:0.85rem; font-weight:700;">CNR NUMBER</div>
            <div style="color:#60a5fa; font-size:1.05rem; font-weight:700; margin-top:6px; word-break:break-all;">{case_row.get('cnr', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        status = case_row.get("status", "Pending")
        bg_color = "rgba(16, 185, 129, 0.2)" if status == "Disposed" else "rgba(245, 158, 11, 0.2)"
        border_color = "#10b981" if status == "Disposed" else "#f59e0b"
        text_color = "#34d399" if status == "Disposed" else "#fbbf24"
        
        st.markdown(f"""
        <div style="background:{bg_color}; border-radius:12px; padding:16px; border:1px solid {border_color}; text-align:center;">
            <div style="color:#cbd5e1; font-size:0.85rem; font-weight:700;">STATUS</div>
            <div style="color:{text_color}; font-size:1.2rem; font-weight:800; margin-top:4px;">{status}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div style="background:#1e293b; border-radius:12px; padding:16px; border:1px solid rgba(255,255,255,0.1); text-align:center;">
            <div style="color:#94a3b8; font-size:0.85rem; font-weight:700;">FILING DATE</div>
            <div style="color:#f8fafc; font-size:1.1rem; font-weight:700; margin-top:6px;">{case_row.get('filing_date', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div style="background:#1e293b; border-radius:12px; padding:16px; border:1px solid rgba(255,255,255,0.1); text-align:center;">
            <div style="color:#94a3b8; font-size:0.85rem; font-weight:700;">REGISTRATION DATE</div>
            <div style="color:#f8fafc; font-size:1.1rem; font-weight:700; margin-top:6px;">{case_row.get('registration_date', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        decision_val = case_row.get('decision_date', '')
        if pd.isna(decision_val) or not str(decision_val).strip() or str(decision_val).lower() == 'none':
            decision_val = "Active Case"
        st.markdown(f"""
        <div style="background:#1e293b; border-radius:12px; padding:16px; border:1px solid rgba(255,255,255,0.1); text-align:center;">
            <div style="color:#94a3b8; font-size:0.85rem; font-weight:700;">DECISION DATE</div>
            <div style="color:#a78bfa; font-size:1.1rem; font-weight:700; margin-top:6px;">{decision_val}</div>
        </div>
        """, unsafe_allow_html=True)

    # Detailed Parties Info
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("⚖️ View Legal Parties, Advocates & Bench Details", expanded=False):
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown(f"**Petitioner:** {case_row.get('petitioner', 'N/A')}")
            st.markdown(f"**Petitioner Advocate:** {case_row.get('petitioner_advocate', 'N/A')}")
            st.markdown(f"**Court Number:** {case_row.get('court_number', 'N/A')}")
        with c_right:
            st.markdown(f"**Respondent:** {case_row.get('respondent', 'N/A')}")
            st.markdown(f"**Respondent Advocate:** {case_row.get('respondent_advocate', 'N/A')}")
            st.markdown(f"**Presiding Bench:** {case_row.get('judge', 'N/A')}")

    # SIGNATURE FEATURE: Case Lifecycle Timeline
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⏱️ Signature Case Lifecycle Timeline")
    st.markdown("Sequential event proceedings with computed gap durations between consecutive court events.")

    case_ev = df_events[df_events["case_identifier"] == selected_case_id].copy() if not df_events.empty else pd.DataFrame()

    if case_ev.empty:
        st.warning("⚠️ No event history records found for this case.")
        return

    case_ev["dt"] = pd.to_datetime(case_ev["event_date"], errors="coerce")
    case_ev = case_ev.dropna(subset=["dt"]).sort_values("dt")
    events_list = case_ev.to_dict("records")

    # Render Visual Timeline Cards using HTML/CSS
    for idx, ev in enumerate(events_list):
        ev_date_str = ev["dt"].strftime("%d %b %Y")
        ev_type = ev.get("event_type", "Proceeding")
        purpose = ev.get("purpose", "Court Proceeding")
        judge = ev.get("judge", "")
        remarks = ev.get("remarks", "")

        if idx > 0:
            prev_dt = events_list[idx - 1]["dt"]
            gap_days = (ev["dt"] - prev_dt).days
            st.markdown(f"""
            <div style="display:flex; align-items:center; margin: 12px 0 12px 42px;">
                <div style="height:24px; border-left:3px dashed #6366f1; margin-right:16px;"></div>
                <span style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color:white; padding:6px 14px; border-radius:20px; font-size:0.9rem; font-weight:700; box-shadow:0 4px 10px rgba(59,130,246,0.3);">
                    ⏳ +{gap_days} days observed gap
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: #1e293b; border-left: 5px solid #38bdf8; border-radius: 12px; padding: 20px 24px; margin-bottom: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <div style="display:flex; justify-between; align-items:center; flex-wrap:wrap;">
                <span style="color:#38bdf8; font-weight:800; font-size:1.2rem;">📅 {ev_date_str}</span>
                <span style="background:rgba(56, 189, 248, 0.15); color:#7dd3fc; padding:4px 12px; border-radius:12px; font-weight:600; font-size:0.85rem; border:1px solid rgba(56, 189, 248, 0.3);">
                    {ev_type}
                </span>
            </div>
            <div style="color: #f1f5f9; font-size: 1.05rem; font-weight:600; margin-top: 10px;">
                <strong>Purpose:</strong> {purpose}
            </div>
            {f'<div style="color: #94a3b8; font-size: 0.95rem; margin-top: 6px;"><strong>Bench:</strong> {judge}</div>' if judge and str(judge).strip() != 'nan' else ''}
            {f'<div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;"><strong>Remarks:</strong> {remarks}</div>' if remarks and str(remarks).strip() != 'nan' else ''}
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 Academic Distinction: Event gap durations measure intervals between recorded court events in public records, rather than administrative judicial delays.")
