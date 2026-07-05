"""
SQLite storage layer for Mission 80 Coach.

This file is responsible only for database access.
It should not contain Streamlit UI code.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]


def _get_database_path() -> Path:
    """
    Resolve the SQLite database path.

    If config.py defines DATABASE_PATH, use it.
    Otherwise, use the default project database location.
    """
    try:
        from config import DATABASE_PATH  # type: ignore

        db_path = Path(DATABASE_PATH)
        if not db_path.is_absolute():
            db_path = ROOT_DIR / db_path
        return db_path
    except Exception:
        return ROOT_DIR / "data" / "database" / "mission80.db"


DB_PATH = _get_database_path()


def get_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection with dictionary-like row access.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """
    Create all required database tables if they do not already exist.
    """
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_date TEXT NOT NULL,
                workout_type TEXT NOT NULL,
                duration_minutes INTEGER DEFAULT 0,
                energy_level INTEGER DEFAULT 0,
                coach_score INTEGER DEFAULT 0,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                exercise_name TEXT NOT NULL,
                source_type TEXT NOT NULL CHECK (
                    source_type IN ('planned', 'extra', 'manual')
                ),
                sets INTEGER,
                reps INTEGER,
                weight_kg REAL,
                duration_minutes INTEGER,
                distance_km REAL,
                calories INTEGER,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id)
                    REFERENCES workout_sessions(id)
                    ON DELETE CASCADE
            );
            """
        )

        conn.commit()


def calculate_coach_score(
    duration_minutes: int,
    completed_planned_count: int,
    extra_count: int,
    manual_count: int,
    energy_level: int,
) -> int:
    """
    Calculate a simple workout coach score.

    This is intentionally simple for now.
    The scoring module can become more advanced later.
    """
    score = 0

    if duration_minutes >= 10:
        score += 20
    if duration_minutes >= 30:
        score += 20
    if completed_planned_count > 0:
        score += min(completed_planned_count * 10, 30)
    if extra_count > 0:
        score += min(extra_count * 5, 10)
    if manual_count > 0:
        score += 10
    if energy_level >= 4:
        score += 10

    return min(score, 100)


def create_workout_session(
    workout_date: str,
    workout_type: str,
    duration_minutes: int = 0,
    energy_level: int = 0,
    coach_score: int = 0,
    notes: str | None = None,
) -> int:
    """
    Create a workout session and return its database ID.
    """
    init_db()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO workout_sessions (
                workout_date,
                workout_type,
                duration_minutes,
                energy_level,
                coach_score,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                workout_date,
                workout_type,
                duration_minutes,
                energy_level,
                coach_score,
                notes,
            ),
        )
        conn.commit()

        session_id = cursor.lastrowid
        if session_id is None:
            raise RuntimeError("Failed to create workout session.")

        return int(session_id)


def add_workout_entry(
    session_id: int,
    exercise_name: str,
    source_type: str,
    sets: int | None = None,
    reps: int | None = None,
    weight_kg: float | None = None,
    duration_minutes: int | None = None,
    distance_km: float | None = None,
    calories: int | None = None,
    notes: str | None = None,
) -> int:
    """
    Add an exercise entry to a workout session.
    """
    init_db()

    if source_type not in {"planned", "extra", "manual"}:
        raise ValueError("source_type must be planned, extra or manual.")

    exercise_name = exercise_name.strip()
    if not exercise_name:
        raise ValueError("Exercise name cannot be empty.")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO workout_entries (
                session_id,
                exercise_name,
                source_type,
                sets,
                reps,
                weight_kg,
                duration_minutes,
                distance_km,
                calories,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                session_id,
                exercise_name,
                source_type,
                sets,
                reps,
                weight_kg,
                duration_minutes,
                distance_km,
                calories,
                notes,
            ),
        )
        conn.commit()

        entry_id = cursor.lastrowid
        if entry_id is None:
            raise RuntimeError("Failed to create workout entry.")

        return int(entry_id)


def save_workout(payload: dict[str, Any]) -> int:
    """
    Save a full workout session with planned, extra and manual entries.

    Expected payload structure:

    {
        "workout_date": "2026-07-05",
        "workout_type": "Strength",
        "duration_minutes": 45,
        "energy_level": 4,
        "notes": "Good session",
        "entries": [
            {
                "exercise_name": "Push-up",
                "source_type": "planned",
                "sets": 3,
                "reps": 12
            }
        ]
    }
    """
    init_db()

    entries = payload.get("entries", [])

    planned_count = sum(
        1 for entry in entries if entry.get("source_type") == "planned"
    )
    extra_count = sum(
        1 for entry in entries if entry.get("source_type") == "extra"
    )
    manual_count = sum(
        1 for entry in entries if entry.get("source_type") == "manual"
    )

    coach_score = calculate_coach_score(
        duration_minutes=int(payload.get("duration_minutes", 0)),
        completed_planned_count=planned_count,
        extra_count=extra_count,
        manual_count=manual_count,
        energy_level=int(payload.get("energy_level", 0)),
    )

    session_id = create_workout_session(
        workout_date=str(payload["workout_date"]),
        workout_type=str(payload.get("workout_type", "Workout")),
        duration_minutes=int(payload.get("duration_minutes", 0)),
        energy_level=int(payload.get("energy_level", 0)),
        coach_score=coach_score,
        notes=payload.get("notes"),
    )

    for entry in entries:
        add_workout_entry(
            session_id=session_id,
            exercise_name=str(entry["exercise_name"]),
            source_type=str(entry["source_type"]),
            sets=entry.get("sets"),
            reps=entry.get("reps"),
            weight_kg=entry.get("weight_kg"),
            duration_minutes=entry.get("duration_minutes"),
            distance_km=entry.get("distance_km"),
            calories=entry.get("calories"),
            notes=entry.get("notes"),
        )

    return session_id


def get_workout_history(limit: int = 20) -> list[dict[str, Any]]:
    """
    Return recent workout sessions with a count of saved exercises.
    """
    init_db()

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                ws.id,
                ws.workout_date,
                ws.workout_type,
                ws.duration_minutes,
                ws.energy_level,
                ws.coach_score,
                ws.notes,
                ws.created_at,
                COUNT(we.id) AS exercise_count
            FROM workout_sessions ws
            LEFT JOIN workout_entries we
                ON ws.id = we.session_id
            GROUP BY ws.id
            ORDER BY ws.workout_date DESC, ws.created_at DESC
            LIMIT ?;
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_workout_entries(session_id: int) -> list[dict[str, Any]]:
    """
    Return all exercise entries for a workout session.
    """
    init_db()

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                session_id,
                exercise_name,
                source_type,
                sets,
                reps,
                weight_kg,
                duration_minutes,
                distance_km,
                calories,
                notes,
                created_at
            FROM workout_entries
            WHERE session_id = ?
            ORDER BY id ASC;
            """,
            (session_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_latest_workout() -> dict[str, Any] | None:
    """
    Return the most recently saved workout session.
    """
    history = get_workout_history(limit=1)

    if not history:
        return None

    latest = history[0]
    latest["entries"] = get_workout_entries(int(latest["id"]))

    return latest


def delete_workout_session(session_id: int) -> None:
    """
    Delete a workout session and its related entries.
    """
    init_db()

    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM workout_sessions
            WHERE id = ?;
            """,
            (session_id,),
        )
        conn.commit()


# Backwards-compatible aliases in case older files call these names.
initialise_database = init_db
initialize_database = init_db
setup_database = init_db
# ---------------------------------------------------------------------
# Nutrition compatibility helpers
# ---------------------------------------------------------------------

DEFAULT_FOOD_DATABASE = [
    {
        "name": "Jollof rice",
        "category": "Nigerian food",
        "portion": "1 medium plate",
        "calories": 450,
        "protein_g": 12,
        "carbs_g": 70,
        "fat_g": 14,
        "notes": "Use smaller portions and add lean protein or vegetables.",
    },
    {
        "name": "Egusi soup",
        "category": "Nigerian food",
        "portion": "1 bowl",
        "calories": 420,
        "protein_g": 18,
        "carbs_g": 12,
        "fat_g": 34,
        "notes": "High calorie due to oil and seeds. Portion control is important.",
    },
    {
        "name": "Grilled chicken breast",
        "category": "Protein",
        "portion": "150g",
        "calories": 250,
        "protein_g": 45,
        "carbs_g": 0,
        "fat_g": 6,
        "notes": "Good lean protein option.",
    },
    {
        "name": "Boiled eggs",
        "category": "Protein",
        "portion": "2 eggs",
        "calories": 155,
        "protein_g": 13,
        "carbs_g": 1,
        "fat_g": 11,
        "notes": "Useful high-protein snack or breakfast item.",
    },
    {
        "name": "Oats",
        "category": "Carbohydrate",
        "portion": "50g dry oats",
        "calories": 190,
        "protein_g": 7,
        "carbs_g": 32,
        "fat_g": 4,
        "notes": "Good breakfast option when portion is controlled.",
    },
    {
        "name": "Greek yoghurt",
        "category": "Protein",
        "portion": "200g",
        "calories": 140,
        "protein_g": 20,
        "carbs_g": 8,
        "fat_g": 0,
        "notes": "Good high-protein low-fat option.",
    },
    {
        "name": "Banana",
        "category": "Fruit",
        "portion": "1 medium banana",
        "calories": 105,
        "protein_g": 1,
        "carbs_g": 27,
        "fat_g": 0,
        "notes": "Good around workouts but still counts towards calories.",
    },
]


def init_food_database() -> None:
    """
    Create and seed the local food database.

    This keeps the Nutrition Centre working while the full nutrition
    module is developed later.
    """
    init_db()

    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS food_database (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT,
                portion TEXT,
                calories INTEGER,
                protein_g REAL,
                carbs_g REAL,
                fat_g REAL,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        for food in DEFAULT_FOOD_DATABASE:
            conn.execute(
                """
                INSERT OR IGNORE INTO food_database (
                    name,
                    category,
                    portion,
                    calories,
                    protein_g,
                    carbs_g,
                    fat_g,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    food["name"],
                    food["category"],
                    food["portion"],
                    food["calories"],
                    food["protein_g"],
                    food["carbs_g"],
                    food["fat_g"],
                    food["notes"],
                ),
            )

        conn.commit()


def get_food_database(search_term: str | None = None) -> list[dict[str, Any]]:
    """
    Return foods from the local food database.

    Returns compatibility fields expected by pages/nutrition.py:
    food_name, category, cuisine, portion_description, calories,
    protein_g, carbs_g and fat_g.
    """
    init_food_database()

    with get_connection() as conn:
        if search_term:
            rows = conn.execute(
                """
                SELECT
                    id,
                    name,
                    category,
                    portion,
                    calories,
                    protein_g,
                    carbs_g,
                    fat_g,
                    notes
                FROM food_database
                WHERE LOWER(COALESCE(name, '')) LIKE LOWER(?)
                   OR LOWER(COALESCE(category, '')) LIKE LOWER(?)
                ORDER BY name ASC;
                """,
                (f"%{search_term}%", f"%{search_term}%"),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT
                    id,
                    name,
                    category,
                    portion,
                    calories,
                    protein_g,
                    carbs_g,
                    fat_g,
                    notes
                FROM food_database
                ORDER BY name ASC;
                """
            ).fetchall()

    foods = []

    for row in rows:
        item = dict(row)

        category = item.get("category") or ""

        if "Nigerian" in category:
            cuisine = "Nigerian"
        else:
            cuisine = "General"

        foods.append(
            {
                "id": item.get("id"),
                "food_name": item.get("name"),
                "name": item.get("name"),
                "category": item.get("category"),
                "cuisine": cuisine,
                "portion_description": item.get("portion"),
                "portion": item.get("portion"),
                "calories": item.get("calories"),
                "protein_g": item.get("protein_g"),
                "carbs_g": item.get("carbs_g"),
                "fat_g": item.get("fat_g"),
                "notes": item.get("notes"),
            }
        )

    return foods


# Backwards-compatible alias.
get_foods = get_food_database
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# User profile compatibility helpers
# ---------------------------------------------------------------------

DEFAULT_USER_PROFILE = {
    "id": 1,
    "name": "Femi",
    "current_weight_kg": 95.0,
    "target_weight_kg": 80.0,
    "height_cm": 0.0,
    "daily_calorie_target": 0,
    "daily_protein_target_g": 0,
    "weekly_workout_target": 4,
}


def _get_table_columns(table_name: str) -> set[str]:
    """
    Return the column names for an existing SQLite table.
    """
    with get_connection() as conn:
        rows = conn.execute(f"PRAGMA table_info({table_name});").fetchall()

    return {row["name"] for row in rows}


def _add_column_if_missing(
    table_name: str,
    column_name: str,
    column_definition: str,
) -> None:
    """
    Add a SQLite column only if it does not already exist.
    """
    columns = _get_table_columns(table_name)

    if column_name not in columns:
        with get_connection() as conn:
            conn.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition};"
            )
            conn.commit()


def init_user_profile() -> None:
    """
    Create and migrate the local user profile table safely.

    This handles older database files that may already have a user_profile
    table with missing columns.
    """
    init_db()

    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY
            );
            """
        )
        conn.commit()

    _add_column_if_missing("user_profile", "name", "TEXT")
    _add_column_if_missing("user_profile", "current_weight_kg", "REAL")
    _add_column_if_missing("user_profile", "target_weight_kg", "REAL")
    _add_column_if_missing("user_profile", "height_cm", "REAL")
    _add_column_if_missing("user_profile", "daily_calorie_target", "INTEGER")
    _add_column_if_missing("user_profile", "daily_protein_target_g", "INTEGER")
    _add_column_if_missing("user_profile", "weekly_workout_target", "INTEGER")
    _add_column_if_missing("user_profile", "created_at", "TEXT")
    _add_column_if_missing("user_profile", "updated_at", "TEXT")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO user_profile (id)
            VALUES (1);
            """
        )

        conn.execute(
            """
            UPDATE user_profile
            SET
                name = COALESCE(name, ?),
                current_weight_kg = COALESCE(current_weight_kg, ?),
                target_weight_kg = COALESCE(target_weight_kg, ?),
                height_cm = COALESCE(height_cm, ?),
                daily_calorie_target = COALESCE(daily_calorie_target, ?),
                daily_protein_target_g = COALESCE(daily_protein_target_g, ?),
                weekly_workout_target = COALESCE(weekly_workout_target, ?),
                created_at = COALESCE(created_at, CURRENT_TIMESTAMP),
                updated_at = COALESCE(updated_at, CURRENT_TIMESTAMP)
            WHERE id = 1;
            """,
            (
                DEFAULT_USER_PROFILE["name"],
                DEFAULT_USER_PROFILE["current_weight_kg"],
                DEFAULT_USER_PROFILE["target_weight_kg"],
                DEFAULT_USER_PROFILE["height_cm"],
                DEFAULT_USER_PROFILE["daily_calorie_target"],
                DEFAULT_USER_PROFILE["daily_protein_target_g"],
                DEFAULT_USER_PROFILE["weekly_workout_target"],
            ),
        )

        conn.commit()


def get_user_profile() -> dict[str, Any]:
    """
    Return the saved user profile.

    Includes compatibility keys for older page files that still expect
    earlier profile field names.
    """
    init_user_profile()

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT
                id,
                name,
                current_weight_kg,
                target_weight_kg,
                height_cm,
                daily_calorie_target,
                daily_protein_target_g,
                weekly_workout_target
            FROM user_profile
            WHERE id = 1;
            """
        ).fetchone()

    if row is None:
        profile = dict(DEFAULT_USER_PROFILE)
    else:
        profile = dict(row)

    current_weight = profile.get("current_weight_kg", 95.0)
    target_weight = profile.get("target_weight_kg", 80.0)

    # Main profile keys.
    profile["current_weight_kg"] = current_weight
    profile["target_weight_kg"] = target_weight

    # Compatibility aliases for existing pages.
    profile["start_weight_kg"] = current_weight
    profile["start_weight"] = current_weight
    profile["current_weight"] = current_weight
    profile["weight"] = current_weight
    profile["goal_weight_kg"] = target_weight
    profile["goal_weight"] = target_weight
    profile["target_weight"] = target_weight

    profile["daily_calories"] = profile.get("daily_calorie_target", 0)
    profile["protein_target_g"] = profile.get("daily_protein_target_g", 0)
    profile["weekly_workouts"] = profile.get("weekly_workout_target", 4)

    return profile


def update_user_profile(
    name: str | None = None,
    current_weight_kg: float | None = None,
    target_weight_kg: float | None = None,
    height_cm: float | None = None,
    daily_calorie_target: int | None = None,
    daily_protein_target_g: int | None = None,
    weekly_workout_target: int | None = None,
) -> None:
    """
    Update the user profile without replacing the whole row.
    """
    init_user_profile()

    existing = get_user_profile()

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE user_profile
            SET
                name = ?,
                current_weight_kg = ?,
                target_weight_kg = ?,
                height_cm = ?,
                daily_calorie_target = ?,
                daily_protein_target_g = ?,
                weekly_workout_target = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = 1;
            """,
            (
                name if name is not None else existing["name"],
                (
                    current_weight_kg
                    if current_weight_kg is not None
                    else existing["current_weight_kg"]
                ),
                (
                    target_weight_kg
                    if target_weight_kg is not None
                    else existing["target_weight_kg"]
                ),
                height_cm if height_cm is not None else existing["height_cm"],
                (
                    daily_calorie_target
                    if daily_calorie_target is not None
                    else existing["daily_calorie_target"]
                ),
                (
                    daily_protein_target_g
                    if daily_protein_target_g is not None
                    else existing["daily_protein_target_g"]
                ),
                (
                    weekly_workout_target
                    if weekly_workout_target is not None
                    else existing["weekly_workout_target"]
                ),
            ),
        )

        conn.commit()


# Backwards-compatible aliases.
save_user_profile = update_user_profile