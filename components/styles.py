"""
Mission 80 Coach
Shared UI Styling
Version 2.0
"""

import streamlit as st

from config import BACKGROUND, CARD, ERROR, PRIMARY, SECONDARY, SUCCESS, TEXT, WARNING


def apply_global_styles() -> None:
    """Apply global CSS styling for Mission 80 Coach."""

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(124, 58, 237, 0.22), transparent 34%),
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.18), transparent 30%),
                {BACKGROUND};
            color: {TEXT};
        }}

        .block-container {{
            padding-top: 1.2rem;
            padding-bottom: 4rem;
            max-width: 1450px;
        }}

        h1, h2, h3, h4, h5, h6, p, span, label, div {{
            color: {TEXT};
        }}

        .mission-hero {{
            padding: 2rem;
            border-radius: 28px;
            background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
            box-shadow: 0 18px 40px rgba(0,0,0,0.28);
            margin-bottom: 1.5rem;
        }}

        .mission-hero h1 {{
            font-size: 2.6rem;
            margin-bottom: 0.4rem;
            color: white !important;
        }}

        .mission-hero p {{
            color: rgba(255,255,255,0.9) !important;
            font-size: 1rem;
            margin-bottom: 0;
        }}

        .metric-card {{
            background: rgba(30, 41, 59, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 22px;
            padding: 1.25rem;
            box-shadow: 0 12px 32px rgba(0,0,0,0.22);
            min-height: 118px;
        }}

        .metric-label {{
            color: #94A3B8 !important;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }}

        .metric-value {{
            color: #F8FAFC !important;
            font-size: 2rem;
            font-weight: 900;
            line-height: 1.1;
        }}

        .metric-subtext {{
            color: #CBD5E1 !important;
            font-size: 0.82rem;
            margin-top: 0.45rem;
        }}

        .content-card {{
            background: rgba(30, 41, 59, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 24px;
            padding: 1.3rem;
            box-shadow: 0 12px 32px rgba(0,0,0,0.20);
            margin-bottom: 1rem;
        }}

        .content-card h2, .content-card h3 {{
            margin-top: 0;
        }}

        .badge {{
            display: inline-block;
            background: rgba(124, 58, 237, 0.18);
            border: 1px solid rgba(124, 58, 237, 0.38);
            color: #DDD6FE !important;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
        }}

        .success-card {{
            border-left: 5px solid {SUCCESS};
        }}

        .warning-card {{
            border-left: 5px solid {WARNING};
        }}

        .error-card {{
            border-left: 5px solid {ERROR};
        }}

        .exercise-row {{
            background: rgba(15, 23, 42, 0.62);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.65rem;
        }}

        .exercise-row strong {{
            color: #F8FAFC !important;
        }}

        div[data-testid="stTabs"] button p {{
            font-weight: 800;
            color: #CBD5E1 !important;
        }}

        div[data-testid="stTabs"] button[aria-selected="true"] p {{
            color: #C4B5FD !important;
        }}

        .stButton > button {{
            border-radius: 14px;
            border: 1px solid rgba(124, 58, 237, 0.45);
            background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
            color: white;
            font-weight: 800;
            padding: 0.55rem 1rem;
        }}

        .stButton > button:hover {{
            border-color: white;
            filter: brightness(1.08);
        }}

        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
        }}

        input, textarea, select {{
            border-radius: 12px !important;
        }}

        @media only screen and (max-width: 768px) {{
            .mission-hero {{
                padding: 1.4rem;
                border-radius: 22px;
            }}

            .mission-hero h1 {{
                font-size: 1.9rem;
            }}

            .metric-card {{
                min-height: auto;
                padding: 1rem;
            }}

            .metric-value {{
                font-size: 1.55rem;
            }}

            .content-card {{
                padding: 1rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str) -> None:
    """Render the main hero banner."""
    st.markdown(
        f"""
        <div class="mission-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, subtext: str = "") -> None:
    """Render a reusable metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def content_card(title: str, body: str, badge: str | None = None) -> None:
    """Render a reusable content card."""
    badge_html = f'<span class="badge">{badge}</span>' if badge else ""

    st.markdown(
        f"""
        <div class="content-card">
            {badge_html}
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def exercise_row(name: str, detail: str = "") -> None:
    """Render an exercise row."""
    st.markdown(
        f"""
        <div class="exercise-row">
            <strong>{name}</strong><br>
            <span>{detail}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )