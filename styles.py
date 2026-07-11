"""
styles.py
-----------
Shared custom CSS injected into every page for a polished, professional
landing-page feel rather than Streamlit's bare defaults. Includes an
animated gradient hero, feature cards, and smooth entrance transitions.
Kept in one place so the look stays consistent across app.py and pages/.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* ---------- Animated gradient hero ---------- */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-wrap {
    position: relative;
    text-align: center;
    padding: 3rem 1.5rem 2.5rem 1.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    background: linear-gradient(120deg, #1a1c2e, #2d1b3d, #1b2d3d, #1a1c2e);
    background-size: 300% 300%;
    animation: gradientShift 12s ease infinite;
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
}

.hero-wrap::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 30% 20%, rgba(255,107,107,0.15), transparent 40%),
                radial-gradient(circle at 70% 80%, rgba(99,102,241,0.15), transparent 40%);
    pointer-events: none;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-icon {
    font-size: 3.2rem;
    animation: fadeInUp 0.6s ease both;
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    margin: 0.3rem 0 0.6rem 0;
    background: linear-gradient(90deg, #FF6B6B, #C084FC, #60A5FA);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: fadeInUp 0.7s ease both;
    animation-delay: 0.05s;
}

.hero-subtitle {
    color: #B8BCC8;
    font-size: 1.08rem;
    max-width: 620px;
    margin: 0 auto;
    animation: fadeInUp 0.8s ease both;
    animation-delay: 0.1s;
}

.hero-badge {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    background: rgba(255, 107, 107, 0.14);
    border: 1px solid rgba(255, 107, 107, 0.3);
    color: #FF9B9B;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 0.9rem;
    animation: fadeInUp 0.5s ease both;
}

/* ---------- Feature cards ---------- */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0 2rem 0;
}

.feature-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
    animation: fadeInUp 0.7s ease both;
}

.feature-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 107, 107, 0.4);
    background: rgba(255,255,255,0.05);
}

.feature-icon {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}

.feature-title {
    font-weight: 700;
    font-size: 0.98rem;
    margin-bottom: 0.3rem;
    color: #F3F4F6;
}

.feature-desc {
    font-size: 0.85rem;
    color: #9CA3AF;
    line-height: 1.4;
}

@media (max-width: 900px) {
    .feature-grid { grid-template-columns: 1fr; }
}

/* ---------- Auth card ---------- */
.auth-card-wrap {
    animation: fadeInUp 0.5s ease both;
}

/* ---------- General polish ---------- */
div[data-testid="stExpander"] {
    border: 1px solid rgba(250, 250, 250, 0.12);
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.02);
    transition: border-color 0.2s ease;
}
div[data-testid="stExpander"]:hover {
    border-color: rgba(255, 107, 107, 0.3);
}

button[kind="primary"] {
    font-weight: 600;
    border-radius: 10px !important;
    box-shadow: 0 2px 14px rgba(255, 75, 75, 0.28);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4);
}

button[data-baseweb="tab"] {
    font-weight: 500;
    padding-top: 0.6rem;
    padding-bottom: 0.6rem;
}

div[data-testid="stFileUploaderDropzone"] {
    border-radius: 14px;
    transition: border-color 0.2s ease;
}

section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #9CA3AF;
}

/* Success/info boxes get a gentle fade-in too */
div[data-testid="stAlert"] {
    animation: fadeInUp 0.4s ease both;
    border-radius: 12px;
}
</style>
"""


def inject_custom_css() -> None:
    """Inject the shared custom CSS block. Call once near the top of each page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, badge: str = None) -> None:
    """
    Render an animated gradient hero section with an optional badge.

    Args:
        title: Main heading text.
        subtitle: Supporting description text below the heading.
        badge: Optional short label shown above the title (e.g. "AI-Powered").
    """
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


def render_feature_cards() -> None:
    """Render the 3-card feature grid used on the landing/auth screen."""
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Smart Skill Analysis</div>
                <div class="feature-desc">Six AI agents extract your strengths, gaps, and skills - tailored to your actual field.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Field-Adaptive Job Matching</div>
                <div class="feature-desc">Ranked job recommendations grounded in your real background, not generic templates.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🗺️</div>
                <div class="feature-title">Personalized Roadmap</div>
                <div class="feature-desc">A 30/60/90-day plan with courses, certifications, and projects to close your gaps.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
