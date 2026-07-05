"""
Mission 80 Coach
Settings Page
"""

import streamlit as st

from components.styles import hero


def render(profile: dict | None) -> None:
    """Render Settings page."""

    hero(
        "Settings ⚙️",
        "Profile, targets and app preferences.",
    )

    st.subheader("User Profile")

    if profile:
        st.json(dict(profile))
    else:
        st.warning("No profile found.")

    st.info("Editable settings will be added after database write functions are connected.")