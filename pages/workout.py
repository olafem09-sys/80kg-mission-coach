"""
Workout Centre page for Mission 80 Coach.

This page handles the Streamlit UI only.
Database logic lives in utils/storage.py.
"""

from __future__ import annotations

from datetime import date
from typing import Any

import streamlit as st

from utils.storage import (
    get_workout_entries,
    get_workout_history,
    init_db,
    save_workout,
)


DEFAULT_PLANNED_EXERCISES = [
    "Push-ups",
    "Bodyweight squats",
    "Dumbbell rows",
    "Plank",
    "Walking",
]


def _load_planned_exercises() -> list[str]:
    """
    Load planned exercises.

    For now, this uses a safe default list.
    Later, this can be connected to utils/workout_data.py properly.
    """
    try:
        from utils.workout_data import get_today_workout  # type: ignore

        today_workout = get_today_workout()

        if isinstance(today_workout, dict):
            exercises = today_workout.get("exercises", [])

            if exercises and isinstance(exercises, list):
                names = []

                for exercise in exercises:
                    if isinstance(exercise, dict):
                        name = exercise.get("name")
                        if name:
                            names.append(str(name))
                    elif isinstance(exercise, str):
                        names.append(exercise)

                if names:
                    return names

    except Exception:
        pass

    return DEFAULT_PLANNED_EXERCISES


def _clean_optional_int(value: int) -> int | None:
    return value if value > 0 else None


def _clean_optional_float(value: float) -> float | None:
    return value if value > 0 else None


def _build_extra_entries(extra_text: str) -> list[dict[str, Any]]:
    """
    Convert the extra exercise text box into database entries.

    One exercise per line.
    """
    entries = []

    for line in extra_text.splitlines():
        exercise_name = line.strip()

        if exercise_name:
            entries.append(
                {
                    "exercise_name": exercise_name,
                    "source_type": "extra",
                }
            )

    return entries


def render(today: Any | None = None) -> None:
    """
    Render the Workout Centre page.
    """
    init_db()

    st.markdown(
        """
        <div style="
            padding: 1.2rem;
            border-radius: 1.2rem;
            background: linear-gradient(135deg, #6D28D9, #9333EA);
            margin-bottom: 1.2rem;
        ">
            <h1 style="margin: 0; color: white;">Workout Centre</h1>
            <p style="margin: 0.4rem 0 0 0; color: #F3E8FF;">
                Save planned workouts, extra exercises and manual training entries.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    planned_exercises = _load_planned_exercises()

    with st.form("save_workout_form", clear_on_submit=True):
        st.subheader("Save today's workout")

        col1, col2 = st.columns(2)

        with col1:
            workout_date = st.date_input("Workout date", value=date.today())
            workout_type = st.selectbox(
                "Workout type",
                [
                    "Strength",
                    "Cardio",
                    "Mobility",
                    "FitXR",
                    "Garage gym",
                    "Walking",
                    "Mixed",
                    "Other",
                ],
            )

        with col2:
            duration_minutes = st.number_input(
                "Duration in minutes",
                min_value=0,
                max_value=300,
                value=30,
                step=5,
            )
            energy_level = st.slider(
                "Energy level",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = very low, 5 = excellent",
            )

        st.divider()

        st.subheader("Planned exercises completed")

        planned_entries: list[dict[str, Any]] = []

        for index, exercise_name in enumerate(planned_exercises):
            completed = st.checkbox(
                exercise_name,
                key=f"planned_completed_{index}",
            )

            if completed:
                col_sets, col_reps, col_weight = st.columns(3)

                with col_sets:
                    sets = st.number_input(
                        f"Sets - {exercise_name}",
                        min_value=0,
                        max_value=20,
                        value=3,
                        step=1,
                        key=f"planned_sets_{index}",
                    )

                with col_reps:
                    reps = st.number_input(
                        f"Reps - {exercise_name}",
                        min_value=0,
                        max_value=200,
                        value=10,
                        step=1,
                        key=f"planned_reps_{index}",
                    )

                with col_weight:
                    weight_kg = st.number_input(
                        f"Weight kg - {exercise_name}",
                        min_value=0.0,
                        max_value=300.0,
                        value=0.0,
                        step=2.5,
                        key=f"planned_weight_{index}",
                    )

                planned_entries.append(
                    {
                        "exercise_name": exercise_name,
                        "source_type": "planned",
                        "sets": _clean_optional_int(int(sets)),
                        "reps": _clean_optional_int(int(reps)),
                        "weight_kg": _clean_optional_float(float(weight_kg)),
                    }
                )

        st.divider()

        st.subheader("Extra exercises")

        extra_text = st.text_area(
            "Extra exercises completed",
            placeholder="Add one exercise per line, for example:\nCycling\nBattle ropes\nSkipping",
        )

        st.divider()

        st.subheader("Manual exercise entry")

        manual_exercise_name = st.text_input(
            "Manual exercise name",
            placeholder="Example: Dumbbell bench press",
        )

        col_manual_1, col_manual_2, col_manual_3 = st.columns(3)

        with col_manual_1:
            manual_sets = st.number_input(
                "Manual sets",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
            )

        with col_manual_2:
            manual_reps = st.number_input(
                "Manual reps",
                min_value=0,
                max_value=200,
                value=0,
                step=1,
            )

        with col_manual_3:
            manual_weight_kg = st.number_input(
                "Manual weight kg",
                min_value=0.0,
                max_value=300.0,
                value=0.0,
                step=2.5,
            )

        col_manual_4, col_manual_5, col_manual_6 = st.columns(3)

        with col_manual_4:
            manual_duration = st.number_input(
                "Manual duration minutes",
                min_value=0,
                max_value=300,
                value=0,
                step=5,
            )

        with col_manual_5:
            manual_distance = st.number_input(
                "Manual distance km",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.5,
            )

        with col_manual_6:
            manual_calories = st.number_input(
                "Manual calories",
                min_value=0,
                max_value=3000,
                value=0,
                step=10,
            )

        notes = st.text_area(
            "Workout notes",
            placeholder="How did the session feel? Any pain, progress or adjustment needed?",
        )

        save_button = st.form_submit_button("Save Workout", use_container_width=True)

    if save_button:
        extra_entries = _build_extra_entries(extra_text)

        manual_entries: list[dict[str, Any]] = []

        if manual_exercise_name.strip():
            manual_entries.append(
                {
                    "exercise_name": manual_exercise_name.strip(),
                    "source_type": "manual",
                    "sets": _clean_optional_int(int(manual_sets)),
                    "reps": _clean_optional_int(int(manual_reps)),
                    "weight_kg": _clean_optional_float(float(manual_weight_kg)),
                    "duration_minutes": _clean_optional_int(int(manual_duration)),
                    "distance_km": _clean_optional_float(float(manual_distance)),
                    "calories": _clean_optional_int(int(manual_calories)),
                }
            )

        all_entries = planned_entries + extra_entries + manual_entries

        if not all_entries:
            st.warning("Add at least one planned, extra or manual exercise before saving.")
        else:
            session_id = save_workout(
                {
                    "workout_date": workout_date.isoformat(),
                    "workout_type": workout_type,
                    "duration_minutes": int(duration_minutes),
                    "energy_level": int(energy_level),
                    "notes": notes.strip() if notes.strip() else None,
                    "entries": all_entries,
                }
            )

            st.success(f"Workout saved successfully. Session ID: {session_id}")

    st.divider()

    st.subheader("Recent workout history")

    history = get_workout_history(limit=10)

    if not history:
        st.info("No workouts saved yet.")
        return

    for workout in history:
        with st.expander(
            f"{workout['workout_date']} — {workout['workout_type']} "
            f"({workout['exercise_count']} exercises)"
        ):
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric("Duration", f"{workout['duration_minutes']} min")

            with col_b:
                st.metric("Energy", f"{workout['energy_level']}/5")

            with col_c:
                st.metric("Coach score", f"{workout['coach_score']}/100")

            if workout.get("notes"):
                st.write(workout["notes"])

            entries = get_workout_entries(int(workout["id"]))

            if entries:
                st.dataframe(
                    entries,
                    use_container_width=True,
                    hide_index=True,
                )


# Compatibility aliases in case app.py uses a different page function name.
show = render
workout_page = render
render_page = render


if __name__ == "__main__":
    render()