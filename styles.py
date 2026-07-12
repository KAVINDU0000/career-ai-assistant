"""
styles.py
-----------
Shared custom CSS for a genuine SaaS-landing-page-style redesign:
two-column hero with a live product mockup, connected step timeline,
upgraded cards, and a split auth layout. Corporate light navy/blue
palette, paired with .streamlit/config.toml for the base theme.
"""

import streamlit as st

NAVY = "#0A3161"
NAVY_DARK = "#082848"
BLUE = "#0A66C2"
LIGHT_BLUE = "#EAF2FD"
TEXT = "#1D2226"
MUTED = "#5E6B7A"
BORDER = "#E0E4E9"

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
}}

.block-container {{
    padding-top: 1.6rem;
    max-width: 1160px;
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ---------- Top brand bar ---------- */
.brand-bar {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.4rem 0 1.2rem 0;
    animation: fadeInUp 0.5s ease both;
}}
.brand-logo {{
    width: 34px;
    height: 34px;
    border-radius: 8px;
    background: linear-gradient(135deg, {NAVY}, {BLUE});
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}}
.brand-name {{
    font-weight: 800;
    font-size: 1.1rem;
    color: {TEXT};
}}

/* ---------- Hero: two-column ---------- */
.hero-section {{
    padding: 1rem 0 1.8rem 0;
    animation: fadeInUp 0.6s ease both;
}}

.hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.32rem 0.85rem;
    border-radius: 6px;
    background: {LIGHT_BLUE};
    border: 1px solid #C7DCF7;
    color: {BLUE};
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin-bottom: 1.1rem;
}}

.hero-title {{
    font-size: 2.7rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 1rem 0;
    color: {TEXT};
    letter-spacing: -0.02em;
}}
.hero-title .accent {{ color: {BLUE}; }}

.hero-subtitle {{
    color: {MUTED};
    font-size: 1.05rem;
    line-height: 1.6;
    margin-bottom: 1.4rem;
    max-width: 480px;
}}

.hero-checklist {{
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
    margin-bottom: 0.5rem;
}}
.hero-check-item {{
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 0.92rem;
    color: {TEXT};
    font-weight: 500;
}}
.hero-check-icon {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: {LIGHT_BLUE};
    color: {BLUE};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 800;
    flex-shrink: 0;
}}

/* ---------- Hero mockup (fake product preview) ---------- */
.mockup-card {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 14px;
    box-shadow: 0 20px 50px rgba(10, 49, 97, 0.14);
    overflow: hidden;
    animation: fadeInUp 0.7s ease both;
    animation-delay: 0.15s;
}}
.mockup-titlebar {{
    background: #F6F7F9;
    border-bottom: 1px solid {BORDER};
    padding: 0.6rem 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}}
.mockup-dot {{ width: 9px; height: 9px; border-radius: 50%; }}
.mockup-body {{ padding: 1.2rem 1.3rem 1.4rem 1.3rem; }}

.mockup-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.7rem;
}}
.mockup-label {{ font-size: 0.8rem; color: {MUTED}; font-weight: 600; }}
.mockup-score {{ font-size: 0.95rem; color: {BLUE}; font-weight: 800; }}

.mockup-bar-track {{
    height: 7px;
    border-radius: 4px;
    background: #EEF1F4;
    overflow: hidden;
    margin-bottom: 1rem;
}}
.mockup-bar-fill {{
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, {BLUE}, {NAVY});
}}

.mockup-chip-row {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }}
.mockup-chip {{
    background: {LIGHT_BLUE};
    color: {BLUE};
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.3rem 0.65rem;
    border-radius: 999px;
}}

.mockup-timeline {{ display: flex; align-items: center; gap: 0.3rem; }}
.mockup-tl-dot {{ width: 8px; height: 8px; border-radius: 50%; background: {BLUE}; }}
.mockup-tl-line {{ flex: 1; height: 2px; background: {BORDER}; }}
.mockup-tl-label {{ font-size: 0.68rem; color: {MUTED}; margin-top: 0.3rem; }}

/* ---------- Stats bar ---------- */
.stats-bar {{
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    margin: 0.5rem 0 2.2rem 0;
    padding: 1.3rem 0.5rem;
    background: {LIGHT_BLUE};
    border-radius: 12px;
    animation: fadeInUp 0.5s ease both;
    animation-delay: 0.2s;
}}
.stat-item {{ text-align: center; }}
.stat-number {{ font-size: 1.5rem; font-weight: 800; color: {NAVY}; }}
.stat-label {{
    font-size: 0.74rem;
    color: {MUTED};
    letter-spacing: 0.03em;
    text-transform: uppercase;
    margin-top: 0.15rem;
}}

/* ---------- Feature cards ---------- */
.section-label {{
    text-align: center;
    color: {BLUE};
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}}
.section-title {{
    text-align: center;
    color: {TEXT};
    font-weight: 800;
    font-size: 1.6rem;
    margin-bottom: 1.6rem;
}}

.feature-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.1rem;
    margin-bottom: 2.4rem;
}}

.feature-card {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-top: 3px solid {BLUE};
    border-radius: 10px;
    padding: 1.6rem 1.3rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: fadeInUp 0.6s ease both;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
.feature-card:nth-child(1) {{ animation-delay: 0.1s; }}
.feature-card:nth-child(2) {{ animation-delay: 0.18s; }}
.feature-card:nth-child(3) {{ animation-delay: 0.26s; }}
.feature-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(10, 102, 194, 0.14);
}}

.feature-icon-circle {{
    width: 50px;
    height: 50px;
    border-radius: 12px;
    background: {LIGHT_BLUE};
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.9rem auto;
    font-size: 1.5rem;
}}
.feature-title {{ font-weight: 700; font-size: 1.02rem; margin-bottom: 0.4rem; color: {TEXT}; }}
.feature-desc {{ font-size: 0.86rem; color: {MUTED}; line-height: 1.5; }}

@media (max-width: 900px) {{
    .feature-grid {{ grid-template-columns: 1fr; }}
    .stats-bar {{ gap: 1.2rem; }}
}}

/* ---------- How it works: connected timeline ---------- */
.howitworks-wrap {{
    position: relative;
    display: flex;
    justify-content: space-between;
    margin: 0 auto 2.6rem auto;
    max-width: 640px;
    animation: fadeInUp 0.6s ease both;
    animation-delay: 0.3s;
}}
.howitworks-wrap::before {{
    content: "";
    position: absolute;
    top: 18px;
    left: 10%;
    right: 10%;
    height: 2px;
    background: {BORDER};
    z-index: 0;
}}
.howitworks-step {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}}
.howitworks-num {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: {BLUE};
    color: white;
    font-weight: 800;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 4px solid #FFFFFF;
    box-shadow: 0 0 0 1px {BORDER};
}}
.howitworks-text {{ font-size: 0.82rem; color: {TEXT}; font-weight: 600; text-align: center; }}

/* ---------- Auth section: split layout ---------- */
.auth-section-wrap {{
    background: {LIGHT_BLUE};
    border-radius: 16px;
    padding: 2.2rem;
    margin-bottom: 1.5rem;
    animation: fadeInUp 0.5s ease both;
    animation-delay: 0.35s;
}}
.auth-value-title {{ font-size: 1.4rem; font-weight: 800; color: {TEXT}; margin-bottom: 0.6rem; }}
.auth-value-text {{ font-size: 0.92rem; color: {MUTED}; line-height: 1.6; margin-bottom: 1.2rem; }}
.auth-value-point {{
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    font-size: 0.87rem;
    color: {TEXT};
    margin-bottom: 0.6rem;
}}

div[data-testid="stForm"] {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 0.5rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}}

.trust-line {{
    text-align: center;
    color: {MUTED};
    font-size: 0.8rem;
    margin-top: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.3rem;
    flex-wrap: wrap;
}}
.trust-line span {{ display: inline-flex; align-items: center; gap: 0.35rem; }}

/* ---------- General polish ---------- */
div[data-testid="stExpander"] {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    background: #FFFFFF;
    transition: border-color 0.2s ease;
}}
div[data-testid="stExpander"]:hover {{ border-color: {BLUE}; }}

button[kind="primary"] {{
    font-weight: 600;
    border-radius: 6px !important;
    background-color: {BLUE} !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
button[kind="primary"]:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(10, 102, 194, 0.3);
}}

button[data-baseweb="tab"] {{
    font-weight: 600;
    padding-top: 0.6rem;
    padding-bottom: 0.6rem;
    color: {MUTED};
}}

div[data-testid="stFileUploaderDropzone"] {{ border-radius: 8px; border-color: {BORDER}; }}

section[data-testid="stSidebar"] {{ background-color: {LIGHT_BLUE}; }}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: {MUTED};
}}

div[data-testid="stAlert"] {{ animation: fadeInUp 0.3s ease both; border-radius: 8px; }}

.app-footer {{
    text-align: center;
    color: {MUTED};
    font-size: 0.78rem;
    margin-top: 2rem;
    padding-top: 1.2rem;
    border-top: 1px solid {BORDER};
}}
</style>
"""


def inject_custom_css() -> None:
    """Inject the shared custom CSS block. Call once near the top of each page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_brand_bar() -> None:
    """Render a small logo + brand name bar at the very top."""
    st.markdown(
        """
        <div class="brand-bar">
            <div class="brand-logo">🧭</div>
            <div class="brand-name">Career AI Assistant</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_two_column() -> None:
    """Render a two-column hero: value prop text on the left, product mockup on the right."""
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="hero-section">
                <div class="hero-badge">✨ MULTI-AGENT AI · FREE TO USE</div>
                <div class="hero-title">Turn your resume into a<br><span class="accent">complete career strategy</span></div>
                <div class="hero-subtitle">Six specialized AI agents analyze your resume and deliver skill
                analysis, job matches, interview prep, and a personalized roadmap - in minutes, not days.</div>
                <div class="hero-checklist">
                    <div class="hero-check-item"><span class="hero-check-icon">✓</span> Field-adaptive - no generic templates</div>
                    <div class="hero-check-item"><span class="hero-check-icon">✓</span> Full report in under 5 minutes</div>
                    <div class="hero-check-item"><span class="hero-check-icon">✓</span> 100% free, no credit card required</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="mockup-card">
                <div class="mockup-titlebar">
                    <div class="mockup-dot" style="background:#FF5F57;"></div>
                    <div class="mockup-dot" style="background:#FEBC2E;"></div>
                    <div class="mockup-dot" style="background:#28C840;"></div>
                </div>
                <div class="mockup-body">
                    <div class="mockup-row">
                        <span class="mockup-label">OVERALL RESUME SCORE</span>
                        <span class="mockup-score">85/100</span>
                    </div>
                    <div class="mockup-bar-track"><div class="mockup-bar-fill" style="width:85%;"></div></div>

                    <div class="mockup-row">
                        <span class="mockup-label">TOP JOB MATCHES</span>
                    </div>
                    <div class="mockup-chip-row">
                        <span class="mockup-chip">AI Engineer · 92%</span>
                        <span class="mockup-chip">Data Scientist · 87%</span>
                        <span class="mockup-chip">ML Engineer · 84%</span>
                    </div>

                    <div class="mockup-row">
                        <span class="mockup-label">LEARNING ROADMAP</span>
                    </div>
                    <div class="mockup-timeline">
                        <div class="mockup-tl-dot"></div><div class="mockup-tl-line"></div>
                        <div class="mockup-tl-dot"></div><div class="mockup-tl-line"></div>
                        <div class="mockup-tl-dot"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span class="mockup-tl-label">30 days</span>
                        <span class="mockup-tl-label">60 days</span>
                        <span class="mockup-tl-label">90 days</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_hero(title: str, subtitle: str, badge: str = None) -> None:
    """Kept for pages that still want a simple single hero banner (e.g. History page)."""
    badge_html = f'<div class="hero-badge">{badge}</div>' if badge else ""
    st.markdown(
        f"""
        <div class="hero-section" style="text-align:center;">
            {badge_html}
            <div class="hero-title" style="font-size:2rem;">{title}</div>
            <div class="hero-subtitle" style="margin:0 auto;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats_bar() -> None:
    """Render a small trust/stats strip under the hero."""
    st.markdown(
        """
        <div class="stats-bar">
            <div class="stat-item"><div class="stat-number">6</div><div class="stat-label">AI Agents</div></div>
            <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">Free to Use</div></div>
            <div class="stat-item"><div class="stat-number">&lt;5 min</div><div class="stat-label">Per Analysis</div></div>
            <div class="stat-item"><div class="stat-number">Private</div><div class="stat-label">Data Stays Yours</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards() -> None:
    """Render the 3-card feature grid, with a section label above it."""
    st.markdown(
        """
        <div class="section-label">WHAT YOU GET</div>
        <div class="section-title">Everything you need to plan your next move</div>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon-circle">🧠</div>
                <div class="feature-title">Smart Skill Analysis</div>
                <div class="feature-desc">Six AI agents extract your strengths, gaps, and skills - tailored to your actual field.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon-circle">🎯</div>
                <div class="feature-title">Field-Adaptive Job Matching</div>
                <div class="feature-desc">Ranked job recommendations grounded in your real background, not generic templates.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon-circle">🗺️</div>
                <div class="feature-title">Personalized Roadmap</div>
                <div class="feature-desc">A 30/60/90-day plan with courses, certifications, and projects to close your gaps.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_how_it_works() -> None:
    """Render a connected 3-step timeline."""
    st.markdown(
        """
        <div class="section-label">GETTING STARTED</div>
        <div class="section-title">Three steps to your career report</div>
        <div class="howitworks-wrap">
            <div class="howitworks-step"><div class="howitworks-num">1</div><div class="howitworks-text">Sign up free</div></div>
            <div class="howitworks-step"><div class="howitworks-num">2</div><div class="howitworks-text">Upload your resume</div></div>
            <div class="howitworks-step"><div class="howitworks-num">3</div><div class="howitworks-text">Get your full report</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render a small footer at the bottom of the page."""
    st.markdown(
        '<div class="app-footer">Built with CrewAI + OpenAI · Career AI Assistant</div>',
        unsafe_allow_html=True,
    )
