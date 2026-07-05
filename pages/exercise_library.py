"""
Mission 80 Coach
Exercise Library Page
"""

import streamlit as st

from components.styles import hero
from utils.workout_data import (
    get_exercises_by_category,
    get_exercise_names,
)


def render() -> None:
    """Render the Exercise Library page."""

    hero(
        "Exercise Library 📚",
        "Browse your exercise database, watch videos and improve your technique.",
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        category = st.selectbox(
            "Category",
            [
                "All",
                "Push",
                "Pull",
                "Legs",
                "Full Body",
                "Core",
                "Cardio",
                "Mobility",
            ],
        )

    with col2:
        search = st.text_input("Search exercise")

    exercises = get_exercises_by_category(category)

    if search:
        term = search.lower()

        exercises = {
            name: details
            for name, details in exercises.items()
            if (
                term in name.lower()
                or term in " ".join(details["equipment"]).lower()
                or term in " ".join(details["muscles"]).lower()
            )
        }

    st.caption(f"{len(exercises)} exercises found")

    for exercise_name in sorted(exercises.keys()):

        details = exercises[exercise_name]

        with st.expander(f"💪 {exercise_name}"):

            c1, c2 = st.columns([2, 1])

            with c1:

                st.write(
                    f"**Primary muscles:** {', '.join(details['muscles'])}"
                )

                st.write(
                    f"**Equipment:** {', '.join(details['equipment'])}"
                )

                st.write(
                    f"**Difficulty:** {details['difficulty']}"
                )

                st.write("### Instructions")

                st.write(details["instructions"])

                st.write("### Coach Tip")

                st.success(details["coach_tip"])

                st.write("### Common Mistakes")

                st.warning(details["common_mistakes"])

                st.write("### Alternatives")

                for alt in details["alternatives"]:
                    st.write(f"• {alt}")

            with c2:

                st.metric("Category", details["category"])

                if details["video"]:
                    st.info("Embedded exercise video")

                    st.video(details["video"])

                else:
                    st.info(
                        "Video coming soon.\n\nYou can add an MP4 into assets/videos."
                    )

    st.divider()

    st.subheader("Quick Find")

    selected = st.selectbox(
        "Jump directly to an exercise",
        sorted(get_exercise_names()),
    )

    if selected:

        st.success(f"Selected: {selected}")