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
from styles import inject_custom_css, render_hero, render_section_label, render_brand_bar
from report_export import markdown_to_docx_bytes, markdown_to_pdf_bytes

st.set_page_config(page_title="CareerCompass · History", page_icon="🗂️", layout="wide")
inject_custom_css()

if not render_auth_gate():
    st.stop()

render_user_badge_and_logout()
render_brand_bar()

render_hero(
    title="🗂️ Report History",
    subtitle="Every past resume analysis you've run, saved automatically.",
    badge="YOUR REPORTS",
)

init_db()

user_id = st.session_state["user"]["id"]
reports = get_all_reports(user_id)

render_section_label(f"{len(reports)} SAVED REPORT(S)" if reports else "NO REPORTS YET")

if not reports:
    st.info("No reports yet - analyze a resume on the main page to see it appear here.")
else:
    for r in reports:
        score_display = f"{int(r['overall_score'])}/100" if r["overall_score"] is not None else "N/A"
        with st.container(border=True):
            with st.expander(
                f"📄 {r['filename']}  —  {r['created_at'].strftime('%Y-%m-%d %H:%M')}  —  Score: {score_display}"
            ):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        label="📝 Download as Word",
                        data=markdown_to_docx_bytes(r["report_markdown"], title="Career Analysis Report"),
                        file_name=f"career_report_{r['id']}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_docx_{r['id']}",
                        use_container_width=True,
                    )
                with col2:
                    st.download_button(
                        label="📕 Download as PDF",
                        data=markdown_to_pdf_bytes(r["report_markdown"], title="Career Analysis Report"),
                        file_name=f"career_report_{r['id']}.pdf",
                        mime="application/pdf",
                        key=f"download_pdf_{r['id']}",
                        use_container_width=True,
                    )
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{r['id']}", use_container_width=True):
                        delete_report(user_id, r["id"])
                        st.rerun()

                st.markdown("---")
                st.markdown(r["report_markdown"])
