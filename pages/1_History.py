"""
pages/1_History.py
---------------------
Streamlit page (auto-detected from the pages/ folder) showing every past
career report, pulled from the SQLite database. Lets the user browse,
reopen, re-download, or delete past analyses without re-running the crew.
"""

import streamlit as st

from config import settings
from database.db import init_db
from database.crud import get_all_reports, get_report_by_id, delete_report

st.set_page_config(page_title="Report History", page_icon="🗂️", layout="wide")
st.title("🗂️ Report History")
st.caption("Every past resume analysis, saved automatically when you run Analyze.")

init_db()

reports = get_all_reports()

if not reports:
    st.info("No reports yet - analyze a resume on the main page to see it appear here.")
else:
    # --- List view: one row per report ---
    st.subheader(f"{len(reports)} report(s)")

    for r in reports:
        score_display = f"{int(r['overall_score'])}/100" if r["overall_score"] is not None else "N/A"
        with st.expander(
            f"📄 {r['filename']}  —  {r['created_at'].strftime('%Y-%m-%d %H:%M')}  —  Score: {score_display}"
        ):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download this report",
                    data=r["report_markdown"],
                    file_name=f"career_report_{r['id']}.md",
                    mime="text/markdown",
                    key=f"download_{r['id']}",
                )
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{r['id']}"):
                    delete_report(r["id"])
                    st.rerun()

            st.markdown("---")
            st.markdown(r["report_markdown"])
