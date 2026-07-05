"""
Mission 80 Coach
Dashboard Page
"""

import streamlit as st

from components.cards import milestone_card, stat_card
from components.styles import content_card, exercise_row, hero
from config import START_WEIGHT, TARGET_WEIGHT
from utils.workout_data import get_today_workout


def render(profile: dict, today: str) -> None:
    """Render dashboard page."""

    today_workout = get_today_workout(today)

    weight_now = profile["start_weight_kg"] if profile else START_WEIGHT
    target_weight = profile["target_weight_kg"] if profile else TARGET_WEIGHT
    remaining = max(0, weight_now - target_weight)
    progress = max(
        0,
        min(
            100,
            (START_WEIGHT - weight_now) / (START_WEIGHT - TARGET_WEIGHT) * 100,
        ),
    )

    hero(
        "Mission 80 Coach 💪",
        "Your training, nutrition and lifestyle coaching dashboard.",
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        stat_card("Current Weight", f"{weight_now:.1f} kg", "Starting point")

    with c2:
        stat_card("Target Weight", f"{target_weight:.1f} kg", "Main goal")

    with c3:
        stat_card("To Lose", f"{remaining:.1f} kg", "Remaining")

    with c4:
        stat_card("Today", today, today_workout["title"])

    st.progress(progress / 100)
    st.caption(f"Mission progress: {progress:.1f}% complete")

    left, right = st.columns([1.4, 1])

    with left:
        content_card(
            "Today’s Workout",
            f"{today_workout['focus']} · Expected duration: {today_workout['duration']}",
            badge=today_workout["title"],
        )

        for exercise in today_workout["exercises"]:
            exercise_row(exercise, "Planned exercise")

    with right:
        milestone_card(weight_now, target_weight)

        content_card(
            "Coach Message",
            "Focus on consistency. If you cannot complete the full session, complete at least 20 minutes.",
            badge="Daily Coach",
        )

        content_card(
            "Nutrition Focus",
            "Protein first. Keep rice portions controlled and aim for at least 2.5 litres of water.",
            badge="Food Coach",
        )