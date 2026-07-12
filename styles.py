"""
styles.py
-----------
Shared custom CSS supporting BOTH a light corporate theme and a full dark
theme, switchable at runtime via a sidebar toggle. Streamlit's own
config.toml only sets a single build-time default theme, so to get a
genuine runtime-switchable light/dark toggle we override Streamlit's core
app containers directly with CSS driven by st.session_state["theme_mode"].
"""

import streamlit as st

# ---------------------------------------------------------------------
# Color palettes for each mode. Every color used anywhere in the custom
# CSS comes from one of these two dicts, selected by the active mode.
# ---------------------------------------------------------------------
LIGHT = {
    "app_bg": "#FFFFFF",
    "panel_bg": "#F3F2EF",
    "card_bg": "#FFFFFF",
    "sidebar_bg": "#EAF2FD",
    "text": "#1D2226",
    "muted": "#5E6B7A",
    "border": "#E0E4E9",
    "navy": "#0A3161",
    "blue": "#0A66C2",
    "light_blue": "#EAF2FD",
    "shadow": "rgba(10, 49, 97, 0.14)",
}

DARK = {
    "app_bg": "#0E1117",
    "panel_bg": "#171B24",
    "card_bg": "#171B24",
    "sidebar_bg": "#12151C",
    "text": "#E5E7EB",
    "muted": "#9AA3B2",
    "border": "#2A2F3D",
    "navy": "#0A3161",
    "blue": "#5EA1FF",
    "light_blue": "#1B2838",
    "shadow": "rgba(0, 0, 0, 0.45)",
}

# The product mockup card always stays dark (like a real app screenshot),
# regardless of overall site mode, for consistent visual contrast.
DARK_BG = "#12151C"
DARK_PANEL = "#1B1F2A"
DARK_BORDER = "#2A2F3D"
DARK_MUTED = "#8B93A5"


def _clean(html: str) -> str:
    """
    Strip leading/trailing whitespace from every line of a multi-line HTML
    string before handing it to st.markdown.

    Markdown treats any line indented 4+ spaces as a preformatted code
    block. Nested HTML written with Python's normal indentation easily
    triggers this, causing part of the markup to render as literal text
    instead of being parsed as HTML. Flattening indentation here prevents
    that regardless of how deeply nested the source looks in the .py file.
    Every render_* function in this module MUST pass its HTML through this
    before calling st.markdown.
    """
    return "\n".join(line.strip() for line in html.strip().splitlines())


def get_theme_mode() -> str:
    """Return the currently active theme mode ('light' or 'dark'), defaulting to light."""
    return st.session_state.get("theme_mode", "light")


def render_theme_toggle() -> str:
    """
    Render a light/dark toggle in the sidebar and return the active mode.

    Must be called before inject_custom_css() so the CSS reflects the
    choice made in this same run.
    """
    with st.sidebar:
        current = get_theme_mode()
        options = ["light", "dark"]
        labels = {"light": "☀️ Light", "dark": "🌙 Dark"}
        choice = st.radio(
            "Theme",
            options=options,
            format_func=lambda o: labels[o],
            index=options.index(current),
            horizontal=True,
            key="theme_mode_radio",
        )
        if choice != current:
            st.session_state["theme_mode"] = choice
            st.rerun()
        st.session_state["theme_mode"] = choice
    return choice


def _build_css(mode: str) -> str:
    c = DARK if mode == "dark" else LIGHT

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
    }}

    header[data-testid="stHeader"] {{
        display: none !important;
    }}

    /* Force Streamlit's core app containers to follow our chosen mode,
       since config.toml only sets one static theme at build time. */
    [data-testid="stAppViewContainer"], .main, body {{
        background-color: {c["app_bg"]} !important;
        color: {c["text"]} !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {c["sidebar_bg"]} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {c["text"]} !important;
    }}
    p, span, div, label, li {{
        color: {c["text"]};
    }}

    .block-container {{
        padding-top: 2.2rem;
        max-width: 1160px;
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ---------- Brand bar ---------- */
    .brand-bar {{
        display: flex; align-items: center; gap: 0.6rem;
        padding: 0.4rem 0 1.2rem 0;
        animation: fadeInUp 0.5s ease both;
    }}
    .brand-logo {{
        width: 34px; height: 34px; border-radius: 8px;
        background: linear-gradient(135deg, {c["navy"]}, {c["blue"]});
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
    }}
    .brand-name {{ font-weight: 800; font-size: 1.1rem; color: {c["text"]}; }}

    /* ---------- Hero ---------- */
    .hero-section {{ padding: 1rem 0 1.8rem 0; animation: fadeInUp 0.6s ease both; }}
    .hero-badge {{
        display: inline-flex; align-items: center; gap: 0.4rem;
        padding: 0.32rem 0.85rem; border-radius: 6px;
        background: {c["light_blue"]}; border: 1px solid {c["border"]};
        color: {c["blue"]}; font-size: 0.76rem; font-weight: 700;
        letter-spacing: 0.03em; margin-bottom: 1.1rem;
    }}
    .hero-title {{
        font-size: 2.7rem; font-weight: 800; line-height: 1.15;
        margin: 0 0 1rem 0; color: {c["text"]}; letter-spacing: -0.02em;
    }}
    .hero-title .accent {{ color: {c["blue"]}; }}
    .hero-subtitle {{
        color: {c["muted"]}; font-size: 1.05rem; line-height: 1.6;
        margin-bottom: 1.4rem; max-width: 480px;
    }}
    .hero-checklist {{ display: flex; flex-direction: column; gap: 0.55rem; margin-bottom: 0.5rem; }}
    .hero-check-item {{
        display: flex; align-items: center; gap: 0.55rem;
        font-size: 0.92rem; color: {c["text"]}; font-weight: 500;
    }}
    .hero-check-icon {{
        width: 20px; height: 20px; border-radius: 50%;
        background: {c["light_blue"]}; color: {c["blue"]};
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 800; flex-shrink: 0;
    }}

    /* ---------- Mockup card: always dark ---------- */
    .mockup-card {{
        background: {DARK_BG}; border: 1px solid {DARK_BORDER}; border-radius: 14px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35); overflow: hidden;
        animation: fadeInUp 0.7s ease both; animation-delay: 0.15s;
    }}
    .mockup-titlebar {{
        background: {DARK_PANEL}; border-bottom: 1px solid {DARK_BORDER};
        padding: 0.6rem 0.9rem; display: flex; align-items: center; gap: 0.4rem;
    }}
    .mockup-dot {{ width: 9px; height: 9px; border-radius: 50%; }}
    .mockup-body {{ padding: 1.2rem 1.3rem 1.4rem 1.3rem; }}
    .mockup-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.7rem; }}
    .mockup-label {{ font-size: 0.8rem; color: {DARK_MUTED}; font-weight: 600; letter-spacing: 0.03em; }}
    .mockup-score {{ font-size: 0.95rem; color: #5EA1FF; font-weight: 800; }}
    .mockup-bar-track {{ height: 7px; border-radius: 4px; background: {DARK_PANEL}; overflow: hidden; margin-bottom: 1rem; }}
    .mockup-bar-fill {{ height: 100%; border-radius: 4px; background: linear-gradient(90deg, #5EA1FF, #A78BFA); }}
    .mockup-chip-row {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }}
    .mockup-chip {{
        background: rgba(94, 161, 255, 0.14); color: #8FBBFF; font-size: 0.72rem;
        font-weight: 700; padding: 0.3rem 0.65rem; border-radius: 999px;
        border: 1px solid rgba(94, 161, 255, 0.25);
    }}
    .mockup-timeline {{ display: flex; align-items: center; gap: 0.3rem; }}
    .mockup-tl-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #5EA1FF; flex-shrink: 0; }}
    .mockup-tl-line {{ flex: 1; height: 2px; background: {DARK_BORDER}; }}
    .mockup-tl-label {{ font-size: 0.68rem; color: {DARK_MUTED}; margin-top: 0.3rem; }}

    /* ---------- Stats bar ---------- */
    .stats-bar {{
        display: flex; justify-content: space-around; flex-wrap: wrap;
        margin: 0.5rem 0 2.2rem 0; padding: 1.3rem 0.5rem;
        background: {c["light_blue"]}; border-radius: 12px;
        animation: fadeInUp 0.5s ease both; animation-delay: 0.2s;
    }}
    .stat-item {{ text-align: center; }}
    .stat-number {{ font-size: 1.5rem; font-weight: 800; color: {c["blue"]}; }}
    .stat-label {{ font-size: 0.74rem; color: {c["muted"]}; letter-spacing: 0.03em; text-transform: uppercase; margin-top: 0.15rem; }}

    /* ---------- Section labels + feature cards ---------- */
    .section-label {{
        text-align: center; color: {c["blue"]}; font-weight: 700; font-size: 0.78rem;
        letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.4rem;
    }}
    .section-title {{ text-align: center; color: {c["text"]}; font-weight: 800; font-size: 1.6rem; margin-bottom: 1.6rem; }}

    .feature-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.1rem; margin-bottom: 2.4rem; }}
    .feature-card {{
        background: {c["card_bg"]}; border: 1px solid {c["border"]}; border-top: 3px solid {c["blue"]};
        border-radius: 10px; padding: 1.6rem 1.3rem; text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: fadeInUp 0.6s ease both; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    .feature-card:nth-child(1) {{ animation-delay: 0.1s; }}
    .feature-card:nth-child(2) {{ animation-delay: 0.18s; }}
    .feature-card:nth-child(3) {{ animation-delay: 0.26s; }}
    .feature-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 28px {c["shadow"]}; }}
    .feature-icon-circle {{
        width: 50px; height: 50px; border-radius: 12px; background: {c["light_blue"]};
        display: flex; align-items: center; justify-content: center; margin: 0 auto 0.9rem auto; font-size: 1.5rem;
    }}
    .feature-title {{ font-weight: 700; font-size: 1.02rem; margin-bottom: 0.4rem; color: {c["text"]}; }}
    .feature-desc {{ font-size: 0.86rem; color: {c["muted"]}; line-height: 1.5; }}

    @media (max-width: 900px) {{
        .feature-grid {{ grid-template-columns: 1fr; }}
        .stats-bar {{ gap: 1.2rem; }}
    }}

    /* ---------- How it works ---------- */
    .howitworks-wrap {{
        position: relative; display: flex; justify-content: space-between;
        margin: 0 auto 2.6rem auto; max-width: 640px;
        animation: fadeInUp 0.6s ease both; animation-delay: 0.3s;
    }}
    .howitworks-wrap::before {{
        content: ""; position: absolute; top: 18px; left: 10%; right: 10%;
        height: 2px; background: {c["border"]}; z-index: 0;
    }}
    .howitworks-step {{ position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; gap: 0.5rem; flex: 1; }}
    .howitworks-num {{
        width: 36px; height: 36px; border-radius: 50%; background: {c["blue"]}; color: white;
        font-weight: 800; font-size: 0.95rem; display: flex; align-items: center; justify-content: center;
        border: 4px solid {c["app_bg"]}; box-shadow: 0 0 0 1px {c["border"]};
    }}
    .howitworks-text {{ font-size: 0.82rem; color: {c["text"]}; font-weight: 600; text-align: center; }}

    /* ---------- Auth section ---------- */
    .auth-section-wrap {{
        background: {c["light_blue"]}; border-radius: 16px; padding: 2.2rem; margin-bottom: 1.5rem;
        animation: fadeInUp 0.5s ease both; animation-delay: 0.35s;
    }}
    .auth-value-title {{ font-size: 1.4rem; font-weight: 800; color: {c["text"]}; margin-bottom: 0.6rem; }}
    .auth-value-text {{ font-size: 0.92rem; color: {c["muted"]}; line-height: 1.6; margin-bottom: 1.2rem; }}
    .auth-value-point {{ display: flex; align-items: flex-start; gap: 0.55rem; font-size: 0.87rem; color: {c["text"]}; margin-bottom: 0.6rem; }}

    div[data-testid="stForm"] {{
        background: {c["card_bg"]} !important; border: 1px solid {c["border"]}; border-radius: 12px;
        padding: 0.5rem; box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }}
    div[data-testid="stForm"] input {{
        background-color: {c["panel_bg"]} !important;
        color: {c["text"]} !important;
    }}

    .trust-line {{
        text-align: center; color: {c["muted"]}; font-size: 0.8rem; margin-top: 1.2rem;
        display: flex; align-items: center; justify-content: center; gap: 1.3rem; flex-wrap: wrap;
    }}
    .trust-line span {{ display: inline-flex; align-items: center; gap: 0.35rem; }}

    /* ---------- General ---------- */
    div[data-testid="stExpander"] {{
        border: 1px solid {c["border"]}; border-radius: 10px; background: {c["card_bg"]};
        transition: border-color 0.2s ease;
    }}
    div[data-testid="stExpander"]:hover {{ border-color: {c["blue"]}; }}

    button[kind="primary"] {{
        font-weight: 600; border-radius: 6px !important; background-color: {c["blue"]} !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    button[kind="primary"]:hover {{ transform: translateY(-1px); box-shadow: 0 4px 14px {c["shadow"]}; }}

    button[data-baseweb="tab"] {{ font-weight: 600; padding-top: 0.6rem; padding-bottom: 0.6rem; color: {c["muted"]}; }}

    div[data-testid="stFileUploaderDropzone"] {{ border-radius: 8px; border-color: {c["border"]}; background: {c["panel_bg"]} !important; }}

    div[data-testid="stAlert"] {{ animation: fadeInUp 0.3s ease both; border-radius: 8px; }}

    .app-footer {{
        text-align: center; color: {c["muted"]}; font-size: 0.78rem;
        margin-top: 2rem; padding-top: 1.2rem; border-top: 1px solid {c["border"]};
    }}
    </style>
    """


def inject_custom_css() -> None:
    """Inject the shared custom CSS block for the currently active theme mode."""
    mode = get_theme_mode()
    st.markdown(_build_css(mode), unsafe_allow_html=True)


def render_brand_bar() -> None:
    """Render a small logo + brand name bar at the very top."""
    st.markdown(
        _clean("""
        <div class="brand-bar">
            <div class="brand-logo">🧭</div>
            <div class="brand-name">Career AI Assistant</div>
        </div>
        """),
        unsafe_allow_html=True,
    )


def render_hero_two_column() -> None:
    """Render a two-column hero: value prop text on the left, product mockup on the right."""
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown(
            _clean("""
            <div class="hero-section">
                <div class="hero-badge">✨ MULTI-AGENT AI · FREE TO USE</div>
                <div class="hero-title">Turn your resume into a<br><span class="accent">complete career strategy</span></div>
                <div class="hero-subtitle">Six specialized AI agents analyze your resume and deliver skill analysis, job matches, interview prep, and a personalized roadmap - in minutes, not days.</div>
                <div class="hero-checklist">
                    <div class="hero-check-item"><span class="hero-check-icon">✓</span> Field-adaptive - no generic templates</div>
                    <div class="hero-check-item"><span class="hero-check-icon">✓</span> Full report in under 5 minutes</div>
                    <div class="hero-check-item"><span class="hero-check-icon">✓</span> 100% free, no credit card required</div>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            _clean("""
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
                        <div class="mockup-tl-dot"></div><div class="mockup-tl-line"></div><div class="mockup-tl-dot"></div><div class="mockup-tl-line"></div><div class="mockup-tl-dot"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span class="mockup-tl-label">30 days</span>
                        <span class="mockup-tl-label">60 days</span>
                        <span class="mockup-tl-label">90 days</span>
                    </div>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )


def render_hero(title: str, subtitle: str, badge: str = None) -> None:
    """Kept for pages that still want a simple single hero banner (e.g. History page)."""
    badge_html = f'<div class="hero-badge">{badge}</div>' if badge else ""
    st.markdown(
        _clean(f"""
        <div class="hero-section" style="text-align:center;">
            {badge_html}
            <div class="hero-title" style="font-size:2rem;">{title}</div>
            <div class="hero-subtitle" style="margin:0 auto;">{subtitle}</div>
        </div>
        """),
        unsafe_allow_html=True,
    )


def render_stats_bar() -> None:
    """Render a small trust/stats strip under the hero."""
    st.markdown(
        _clean("""
        <div class="stats-bar">
            <div class="stat-item"><div class="stat-number">6</div><div class="stat-label">AI Agents</div></div>
            <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">Free to Use</div></div>
            <div class="stat-item"><div class="stat-number">&lt;5 min</div><div class="stat-label">Per Analysis</div></div>
            <div class="stat-item"><div class="stat-number">Private</div><div class="stat-label">Data Stays Yours</div></div>
        </div>
        """),
        unsafe_allow_html=True,
    )


def render_feature_cards() -> None:
    """Render the 3-card feature grid, with a section label above it."""
    st.markdown(
        _clean("""
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
        """),
        unsafe_allow_html=True,
    )


def render_how_it_works() -> None:
    """Render a connected 3-step timeline."""
    st.markdown(
        _clean("""
        <div class="section-label">GETTING STARTED</div>
        <div class="section-title">Three steps to your career report</div>
        <div class="howitworks-wrap">
            <div class="howitworks-step"><div class="howitworks-num">1</div><div class="howitworks-text">Sign up free</div></div>
            <div class="howitworks-step"><div class="howitworks-num">2</div><div class="howitworks-text">Upload your resume</div></div>
            <div class="howitworks-step"><div class="howitworks-num">3</div><div class="howitworks-text">Get your full report</div></div>
        </div>
        """),
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render a small footer at the bottom of the page."""
    st.markdown(
        _clean('<div class="app-footer">Built with CrewAI + OpenAI · Career AI Assistant</div>'),
        unsafe_allow_html=True,
    )
