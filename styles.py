"""
styles.py
-----------
Shared custom CSS injected into every page for a polished, professional
landing-page feel. Includes an animated gradient hero, staggered feature
card entrances, a "how it works" flow, trust signals, and smooth
transitions throughout. Kept in one place so the look stays consistent
across app.py and pages/.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 1140px;
}

/* ---------- Animated gradient hero ---------- */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes floatOrb {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50%      { transform: translate(20px, -15px) scale(1.05); }
}

.hero-wrap {
    position: relative;
    text-align: center;
    padding: 3.2rem 1.5rem 2.6rem 1.5rem;
    border-radius: 22px;
    margin-bottom: 1.6rem;
    background: linear-gradient(120deg, #17182b, #2a1a3a, #16283a, #17182b);
    background-size: 300% 300%;
    animation: gradientShift 14s ease infinite;
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
}

.hero-wrap::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 25% 15%, rgba(255,107,107,0.18), transparent 42%),
                radial-gradient(circle at 75% 85%, rgba(99,102,241,0.18), transparent 42%),
                radial-gradient(circle at 50% 50%, rgba(192,132,252,0.08), transparent 60%);
    pointer-events: none;
    animation: floatOrb 10s ease-in-out infinite;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-icon { font-size: 3.2rem; }

.hero-title {
    font-size: 2.75rem;
    font-weight: 800;
    margin: 0.3rem 0 0.7rem 0;
    background: linear-gradient(90deg, #FF6B6B, #C084FC, #60A5FA);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: fadeInUp 0.7s ease both;
    animation-delay: 0.05s;
    letter-spacing: -0.01em;
}

.hero-subtitle {
    color: #C3C7D4;
    font-size: 1.1rem;
    max-width: 660px;
    margin: 0 auto;
    animation: fadeInUp 0.8s ease both;
    animation-delay: 0.12s;
    line-height: 1.55;
}

.hero-badge {
    display: inline-block;
    padding: 0.32rem 0.95rem;
    border-radius: 999px;
    background: rgba(255, 107, 107, 0.14);
    border: 1px solid rgba(255, 107, 107, 0.32);
    color: #FF9B9B;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
    animation: fadeInUp 0.5s ease both;
}

/* ---------- Trust / stats bar ---------- */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    flex-wrap: wrap;
    margin: 0 0 2rem 0;
    animation: fadeInUp 0.6s ease both;
    animation-delay: 0.2s;
}
.stat-item {
    text-align: center;
}
.stat-number {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, #FF6B6B, #C084FC);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.stat-label {
    font-size: 0.78rem;
    color: #8B90A0;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    margin-top: 0.1rem;
}

/* ---------- Feature cards, staggered entrance ---------- */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.1rem;
    margin: 0 0 2.2rem 0;
}

.feature-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.09);
    border-top: 2px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 1.6rem 1.3rem;
    text-align: center;
    transition: transform 0.28s ease, border-color 0.28s ease, background 0.28s ease, box-shadow 0.28s ease;
    animation: fadeInUp 0.7s ease both;
}
.feature-card:nth-child(1) { animation-delay: 0.15s; }
.feature-card:nth-child(2) { animation-delay: 0.28s; }
.feature-card:nth-child(3) { animation-delay: 0.41s; }

.feature-card:hover {
    transform: translateY(-6px);
    border-color: rgba(255, 107, 107, 0.45);
    border-top-color: #FF6B6B;
    background: rgba(255,255,255,0.055);
    box-shadow: 0 12px 30px rgba(255, 107, 107, 0.12);
}

.feature-icon {
    font-size: 1.9rem;
    margin-bottom: 0.55rem;
}

.feature-title {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.35rem;
    color: #F3F4F6;
}

.feature-desc {
    font-size: 0.86rem;
    color: #9CA3AF;
    line-height: 1.45;
}

@media (max-width: 900px) {
    .feature-grid { grid-template-columns: 1fr; }
    .stats-bar { gap: 1.5rem; }
}

/* ---------- How it works ---------- */
.howitworks-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin: 0 0 2.4rem 0;
    flex-wrap: wrap;
    animation: fadeInUp 0.7s ease both;
    animation-delay: 0.5s;
}
.howitworks-step {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 0.7rem 1.2rem;
}
.howitworks-num {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: linear-gradient(135deg, #FF6B6B, #C084FC);
    color: white;
    font-weight: 700;
    font-size: 0.82rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.howitworks-text {
    font-size: 0.87rem;
    color: #D1D5DB;
    font-weight: 500;
    white-space: nowrap;
}
.howitworks-arrow {
    color: #FF6B6B;
    font-size: 1.1rem;
    opacity: 0.6;
}

/* ---------- Auth card ---------- */
.auth-card-wrap {
    animation: fadeInUp 0.6s ease both;
    animation-delay: 0.55s;
    position: relative;
}

.trust-line {
    text-align: center;
    color: #6B7280;
    font-size: 0.82rem;
    margin-top: 1.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.4rem;
    flex-wrap: wrap;
}
.trust-line span {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
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

div[data-testid="stAlert"] {
    animation: fadeInUp 0.4s ease both;
    border-radius: 12px;
}

/* Footer */
.app-footer {
    text-align: center;
    color: #4B5563;
    font-size: 0.78rem;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}
</style>
"""


def inject_custom_css() -> None:
    """Inject the shared custom CSS block. Call once near the top of each page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, badge: str = None) -> None:
    """Render an animated gradient hero section with an optional badge."""
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
