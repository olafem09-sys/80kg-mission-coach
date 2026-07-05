from utils.storage import (
    get_latest_workout,
    get_workout_history,
    init_db,
    save_workout,
)


def test_workout_storage_smoke():
    init_db()

    session_id = save_workout(
        {
            "workout_date": "2026-07-05",
            "workout_type": "Strength",
            "duration_minutes": 35,
            "energy_level": 4,
            "notes": "Smoke test workout",
            "entries": [
                {
                    "exercise_name": "Push-ups",
                    "source_type": "planned",
                    "sets": 3,
                    "reps": 12,
                },
                {
                    "exercise_name": "Walking",
                    "source_type": "extra",
                    "duration_minutes": 20,
                },
                {
                    "exercise_name": "Dumbbell curl",
                    "source_type": "manual",
                    "sets": 3,
                    "reps": 10,
                    "weight_kg": 10,
                },
            ],
        }
    )

    assert session_id > 0

    history = get_workout_history(limit=5)
    assert len(history) > 0

    latest = get_latest_workout()
    assert latest is not None
    assert len(latest["entries"]) > 0