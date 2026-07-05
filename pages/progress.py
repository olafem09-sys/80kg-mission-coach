"""
Mission 80 Coach
Progress Page
"""

import streamlit as st

from components.cards import stat_card
from components.styles import content_card, hero
from config import START_WEIGHT, TARGET_WEIGHT


def render() -> None:
    """Render Progress Centre page."""

    hero(
        "Progress Centre 📈",
        "Track your weight, measurements and transformation progress.",
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        stat_card("Start Weight", f"{START_WEIGHT:.1f} kg")

    with c2:
        stat_card("Target Weight", f"{TARGET_WEIGHT:.1f} kg")

    with c3:
        stat_card("Total Goal", f"{START_WEIGHT - TARGET_WEIGHT:.1f} kg loss")

    content_card(
        "Progress Tracking",
        "Weight logs, measurements, progress photos and trend charts will be added in the Progress sprint.",
        badge="Progress",
    )

    st.subheader("Coming next")
    st.write("- Weight logging")
    st.write("- Waist, chest, arms and leg measurements")
    st.write("- Progress charts")
    st.write("- Weekly review")