"""
pages/1_History.py
---------------------
Streamlit page showing the logged-in user's past career reports, pulled
from the SQLite database and scoped strictly to their own account.
"""

import streamlit as st

from database.db import init_db
from database.crud import get_all_reports, delete_report
from auth_ui import render_auth_gate, render_user_badge_and_logout
from styles import inject_custom_css, render_hero, render_theme_toggle

st.set_page_config(page_title="Report History", page_icon="🗂️", layout="wide")
render_theme_toggle()
inject_custom_css()

if not render_auth_gate():
    st.stop()

render_user_badge_and_logout()

render_hero(
    title="🗂️ Report History",
    subtitle="Every past resume analysis you've run, saved automatically.",
    badge="YOUR REPORTS",
)

init_db()

user_id = st.session_state["user"]["id"]
reports = get_all_reports(user_id)

if not reports:
    st.info("No reports yet - analyze a resume on the main page to see it appear here.")
else:
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
                    delete_report(user_id, r["id"])
                    st.rerun()

            st.markdown("---")
            st.markdown(r["report_markdown"])
