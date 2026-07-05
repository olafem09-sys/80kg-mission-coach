"""
Mission 80 Coach
Reusable UI Cards
Version 2.0
"""

import streamlit as st


def stat_card(title: str, value: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtext">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def coach_card(title: str, message: str, badge: str = "Coach") -> None:
    st.markdown(
        f"""
        <div class="content-card">
            <span class="badge">{badge}</span>
            <h3>{title}</h3>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def action_card(title: str, items: list[str]) -> None:
    st.markdown(
        f"""
        <div class="content-card">
            <h3>{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for item in items:
        st.markdown(
            f"""
            <div class="exercise-row">
                <strong>{item}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


def milestone_card(weight_now: float, target_weight: float) -> None:
    remaining = max(0, weight_now - target_weight)

    st.markdown(
        f"""
        <div class="content-card">
            <span class="badge">Mission Progress</span>
            <h3>{weight_now:.1f} kg → {target_weight:.1f} kg</h3>
            <p><strong>{remaining:.1f} kg</strong> left to reach your target.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )