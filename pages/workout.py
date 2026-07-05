"""
Mission 80 Coach
Workout Page
"""

import streamlit as st

from components.styles import hero
from utils.workout_data import get_exercise_names, get_today_workout


def render(today: str) -> None:
    """Render workout page."""

    today_workout = get_today_workout(today)

    hero(
        "Workout Centre 💪",
        "Track today’s planned workout and add extra exercises.",
    )

    st.subheader(f"{today}: {today_workout['title']}")
    st.write(today_workout["focus"])

    completed = []

    for exercise in today_workout["exercises"]:
        if st.checkbox(exercise):
            completed.append(exercise)

    st.divider()

    st.subheader("Add Extra Exercises")

    extra = st.multiselect(
        "Choose extra exercises completed today",
        get_exercise_names(),
    )

    manual = st.text_input("Manual exercise entry if not listed")

    duration = st.number_input("Workout duration, minutes", 0, 240, 0)
    fitxr_minutes = st.number_input("FitXR minutes", 0, 180, 0)
    fitxr_calories = st.number_input("FitXR calories", 0, 2000, 0)
    notes = st.text_area("Workout notes")

    if st.button("Save Workout"):
        st.success("Workout captured. Database save will be connected next.")

        st.write("**Completed planned exercises:**", completed)
        st.write("**Extra exercises:**", extra)

        if manual:
            st.write("**Manual exercise:**", manual)

        st.write("**Duration:**", duration)
        st.write("**FitXR:**", f"{fitxr_minutes} mins · {fitxr_calories} calories")

        if notes:
            st.write("**Notes:**", notes)