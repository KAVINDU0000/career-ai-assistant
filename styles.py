"""
styles.py
-----------
Shared custom CSS for a clean, corporate, LinkedIn-style light theme:
navy/blue accents, white cards, subtle shadows, restrained typography.
Paired with .streamlit/config.toml, which sets the actual Streamlit
theme base to light so the whole app (not just injected HTML) matches.
"""

import streamlit as st

NAVY = "#0A3161"
BLUE = "#0A66C2"
LIGHT_BLUE = "#E8F0FE"
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
    padding-top: 2rem;
    max-width: 1120px;
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ---------- Hero: solid navy banner, clean and corporate ---------- */
.hero-wrap {{
    position: relative;
    text-align: center;
    padding: 3rem 1.5rem 2.6rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 1.6rem;
    background: linear-gradient(135deg, {NAVY} 0%, #123A73 100%);
    border: 1px solid {NAVY};
    box-shadow: 0 4px 24px rgba(10, 49, 97, 0.15);
}}

.hero-badge {{
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 6px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    color: #FFFFFF;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
    animation: fadeInUp 0.5s ease both;
}}

.hero-title {{
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0.2rem 0 0.7rem 0;
    color: #FFFFFF;
    letter-spacing: -0.01em;
    animation: fadeInUp 0.6s ease both;
    animation-delay: 0.05s;
}}

.hero-subtitle {{
    color: #C9D6E8;
    font-size: 1.05rem;
    max-width: 640px;
    margin: 0 auto;
    line-height: 1.55;
    animation: fadeInUp 0.7s ease both;
    animation-delay: 0.1s;
}}

/* ---------- Stats bar ---------- */
.stats-bar {{
    display: flex;
    justify-content: center;
    gap: 2.8rem;
    flex-wrap: wrap;
    margin: 0 0 2rem 0;
    padding: 1.1rem 0;
    border-bottom: 1px solid {BORDER};
    animation: fadeInUp 0.5s ease both;
    animation-delay: 0.15s;
}}
.stat-item {{ text-align: center; }}
.stat-number {{
    font-size: 1.4rem;
    font-weight: 800;
    color: {BLUE};
}}
.stat-label {{
    font-size: 0.75rem;
    color: {MUTED};
    letter-spacing: 0.03em;
    text-transform: uppercase;
    margin-top: 0.1rem;
}}

/* ---------- Feature cards: white, subtle border, blue icon circles ---------- */
.feature-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.1rem;
    margin: 0 0 2.2rem 0;
}}

.feature-card {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1.6rem 1.3rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    animation: fadeInUp 0.6s ease both;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
.feature-card:nth-child(1) {{ animation-delay: 0.15s; }}
.feature-card:nth-child(2) {{ animation-delay: 0.24s; }}
.feature-card:nth-child(3) {{ animation-delay: 0.33s; }}

.feature-card:hover {{
    transform: translateY(-3px);
    border-color: {BLUE};
    box-shadow: 0 8px 24px rgba(10, 102, 194, 0.12);
}}

.feature-icon-circle {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: {LIGHT_BLUE};
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.8rem auto;
    font-size: 1.4rem;
}}

.feature-title {{
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.4rem;
    color: {TEXT};
}}

.feature-desc {{
    font-size: 0.86rem;
    color: {MUTED};
    line-height: 1.5;
}}

@media (max-width: 900px) {{
    .feature-grid {{ grid-template-columns: 1fr; }}
    .stats-bar {{ gap: 1.5rem; }}
}}

/* ---------- How it works ---------- */
.howitworks-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin: 0 0 2.4rem 0;
    flex-wrap: wrap;
    animation: fadeInUp 0.6s ease both;
    animation-delay: 0.4s;
}}
.howitworks-step {{
    display: flex;
    align-items: center;
    gap: 0.7rem;
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 0.65rem 1.1rem;
}}
.howitworks-num {{
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: {BLUE};
    color: white;
    font-weight: 700;
    font-size: 0.78rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}}
.howitworks-text {{
    font-size: 0.86rem;
    color: {TEXT};
    font-weight: 500;
    white-space: nowrap;
}}
.howitworks-arrow {{
    color: {BLUE};
    font-size: 1.1rem;
    opacity: 0.55;
}}

/* ---------- Auth card ---------- */
.auth-card-wrap {{
    animation: fadeInUp 0.5s ease both;
    animation-delay: 0.45s;
}}

div[data-testid="stForm"] {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 0.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}}

.trust-line {{
    text-align: center;
    color: {MUTED};
    font-size: 0.82rem;
    margin-top: 1.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.4rem;
    flex-wrap: wrap;
}}
.trust-line span {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}}

/* ---------- General polish ---------- */
div[data-testid="stExpander"] {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    background: #FFFFFF;
    transition: border-color 0.2s ease;
}}
div[data-testid="stExpander"]:hover {{
    border-color: {BLUE};
}}

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

div[data-testid="stFileUploaderDropzone"] {{
    border-radius: 8px;
    border-color: {BORDER};
}}

section[data-testid="stSidebar"] {{
    background-color: {LIGHT_BLUE};
}}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: {MUTED};
}}

div[data-testid="stAlert"] {{
    animation: fadeInUp 0.3s ease both;
    border-radius: 8px;
}}

.app-footer {{
    text-align: center;
    color: {MUTED};
    font-size: 0.78rem;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid {BORDER};
}}
</style>
"""


def inject_custom_css() -> None:
    """Inject the shared custom CSS block. Call once near the top of each page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, badge: str = None) -> None:
    """Render a solid navy corporate-style hero banner with an optional badge."""
    badge_html = f'<div class="hero-badge">{badge}</div>' if badge else ""
    st.markdown(
        f"""
        <div class="hero-wrap">
            {badge_html}
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats_bar() -> None:
    """Render a small trust/stats strip under the hero."""
    st.markdown(
        """
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-number">6</div>
                <div class="stat-label">AI Agents</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">100%</div>
                <div class="stat-label">Free to Use</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">&lt;5 min</div>
                <div class="stat-label">Per Analysis</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">Private</div>
                <div class="stat-label">Your Data Stays Yours</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards() -> None:
    """Render the 3-card feature grid used on the landing/auth screen."""
    st.markdown(
        """
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
    """Render a horizontal 3-step 'how it works' flow."""
    st.markdown(
        """
        <div class="howitworks-wrap">
            <div class="howitworks-step">
                <div class="howitworks-num">1</div>
                <div class="howitworks-text">Sign up free</div>
            </div>
            <div class="howitworks-arrow">→</div>
            <div class="howitworks-step">
                <div class="howitworks-num">2</div>
                <div class="howitworks-text">Upload your resume</div>
            </div>
            <div class="howitworks-arrow">→</div>
            <div class="howitworks-step">
                <div class="howitworks-num">3</div>
                <div class="howitworks-text">Get your full report</div>
            </div>
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
