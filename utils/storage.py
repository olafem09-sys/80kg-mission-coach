"""
Mission 80 Coach
Storage Layer
SQLite database foundation
Version: 2.0
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from config import BACKUP_DIR, DATABASE_DIR, DATABASE_FILE


def ensure_directories() -> None:
    """Ensure required data folders exist."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite database connection."""
    ensure_directories()
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def initialise_database() -> None:
    """Create core database tables if they do not already exist."""
    ensure_directories()

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT DEFAULT 'Femi',
                age INTEGER DEFAULT 36,
                height_cm REAL DEFAULT 163,
                start_weight_kg REAL DEFAULT 95,
                target_weight_kg REAL DEFAULT 80,
                training_preference TEXT DEFAULT 'Morning workouts',
                nutrition_preference TEXT DEFAULT 'Nigerian meals',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weight_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date TEXT NOT NULL,
                weight_kg REAL NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date TEXT NOT NULL,
                workout_type TEXT,
                workout_title TEXT,
                completed INTEGER DEFAULT 0,
                duration_minutes INTEGER DEFAULT 0,
                fitxr_minutes INTEGER DEFAULT 0,
                fitxr_calories INTEGER DEFAULT 0,
                steps INTEGER DEFAULT 0,
                energy_score INTEGER DEFAULT 5,
                notes TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS exercise_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id INTEGER,
                exercise_name TEXT NOT NULL,
                exercise_source TEXT DEFAULT 'planned',
                sets INTEGER,
                reps INTEGER,
                weight_kg REAL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (workout_id) REFERENCES workout_log(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS meal_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date TEXT NOT NULL,
                meal_time TEXT,
                meal_name TEXT,
                meal_category TEXT,
                calories_estimate INTEGER,
                protein_g REAL,
                carbs_g REAL,
                fat_g REAL,
                meal_score INTEGER,
                notes TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS food_database (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name TEXT NOT NULL,
                category TEXT,
                cuisine TEXT DEFAULT 'General',
                portion_description TEXT,
                calories INTEGER,
                protein_g REAL,
                carbs_g REAL,
                fat_g REAL,
                fibre_g REAL,
                is_user_favourite INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date TEXT NOT NULL UNIQUE,
                water_litres REAL DEFAULT 0,
                protein_grams REAL DEFAULT 0,
                steps INTEGER DEFAULT 0,
                sleep_hours REAL,
                mood_score INTEGER,
                stress_score INTEGER,
                coach_score INTEGER,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                achievement_key TEXT NOT NULL UNIQUE,
                achievement_name TEXT NOT NULL,
                description TEXT,
                unlocked INTEGER DEFAULT 0,
                unlocked_at TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS app_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT NOT NULL UNIQUE,
                setting_value TEXT,
                updated_at TEXT NOT NULL
            )
            """
        )

        conn.commit()

    seed_default_profile()
    seed_food_database()
    seed_default_achievements()


def now_iso() -> str:
    """Return current timestamp as ISO string."""
    return datetime.now().isoformat(timespec="seconds")


def seed_default_profile() -> None:
    """Create the default user profile if missing."""
    with get_connection() as conn:
        existing = conn.execute("SELECT id FROM user_profile LIMIT 1").fetchone()

        if existing:
            return

        timestamp = now_iso()

        conn.execute(
            """
            INSERT INTO user_profile (
                name, age, height_cm, start_weight_kg, target_weight_kg,
                training_preference, nutrition_preference, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Femi",
                36,
                163,
                95,
                80,
                "Morning workouts",
                "Nigerian meals",
                timestamp,
                timestamp,
            ),
        )
        conn.commit()


def seed_food_database() -> None:
    """Seed starter food database, including Nigerian meals."""
    starter_foods = [
        ("Eggs", "Protein", "General", "1 large egg", 70, 6, 1, 5, 0),
        ("Soda Bread", "Carbs", "General", "1 medium slice", 180, 6, 32, 3, 2),
        ("Rice and Stew", "Main Meal", "Nigerian", "1 fist rice + stew", 550, 25, 65, 18, 4),
        ("Jollof Rice", "Main Meal", "Nigerian", "1 medium plate", 600, 20, 80, 20, 4),
        ("Moi Moi", "Protein", "Nigerian", "1 wrap/portion", 250, 14, 28, 8, 5),
        ("Beans", "Main Meal", "Nigerian", "1 medium bowl", 380, 20, 55, 8, 12),
        ("Grilled Chicken", "Protein", "General", "1 medium portion", 250, 35, 0, 10, 0),
        ("Grilled Fish", "Protein", "General", "1 medium portion", 220, 32, 0, 8, 0),
        ("Plantain", "Carbs", "Nigerian", "1 small portion", 250, 2, 45, 8, 3),
        ("Yam", "Carbs", "Nigerian", "1 medium portion", 300, 4, 68, 1, 5),
        ("Egusi Soup", "Soup", "Nigerian", "1 bowl", 450, 25, 12, 35, 4),
        ("Efo Riro", "Soup", "Nigerian", "1 bowl", 320, 22, 10, 22, 5),
        ("Pepper Soup", "Soup", "Nigerian", "1 bowl", 250, 30, 6, 10, 2),
        ("Greek Yoghurt", "Protein", "General", "1 pot", 150, 15, 8, 5, 0),
        ("Oats", "Breakfast", "General", "1 bowl", 300, 10, 50, 6, 7),
    ]

    with get_connection() as conn:
        existing = conn.execute("SELECT COUNT(*) AS count FROM food_database").fetchone()["count"]

        if existing > 0:
            return

        timestamp = now_iso()

        conn.executemany(
            """
            INSERT INTO food_database (
                food_name, category, cuisine, portion_description,
                calories, protein_g, carbs_g, fat_g, fibre_g, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [food + (timestamp,) for food in starter_foods],
        )
        conn.commit()


def seed_default_achievements() -> None:
    """Seed starter achievement badges."""
    achievements = [
        ("first_workout", "First Workout", "Complete your first logged workout."),
        ("five_workouts", "5 Workout Club", "Complete 5 workouts."),
        ("ten_workouts", "10 Workout Club", "Complete 10 workouts."),
        ("weight_92", "92kg Club", "Reach 92 kg or below."),
        ("weight_90", "90kg Club", "Reach 90 kg or below."),
        ("weight_85", "85kg Club", "Reach 85 kg or below."),
        ("mission_complete", "Mission Complete", "Reach your 80 kg target."),
    ]

    with get_connection() as conn:
        timestamp = now_iso()

        for key, name, description in achievements:
            conn.execute(
                """
                INSERT OR IGNORE INTO achievements (
                    achievement_key, achievement_name, description, unlocked, unlocked_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (key, name, description, 0, None),
            )

        conn.commit()


def fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    """Run a SELECT query and return rows as dictionaries."""
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def fetch_one(query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    """Run a SELECT query and return one row as a dictionary."""
    with get_connection() as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None


def execute_query(query: str, params: tuple[Any, ...] = ()) -> int:
    """Run INSERT/UPDATE/DELETE and return the affected row id."""
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid


def get_user_profile() -> dict[str, Any] | None:
    """Return the current user profile."""
    initialise_database()
    return fetch_one("SELECT * FROM user_profile LIMIT 1")


def get_food_database() -> list[dict[str, Any]]:
    """Return food database records."""
    initialise_database()
    return fetch_all("SELECT * FROM food_database ORDER BY cuisine, category, food_name")


def get_recent_workouts(limit: int = 10) -> list[dict[str, Any]]:
    """Return recent workouts."""
    initialise_database()
    return fetch_all(
        """
        SELECT *
        FROM workout_log
        ORDER BY log_date DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )


def create_database_backup() -> Path | None:
    """Create a simple timestamped backup of the SQLite database."""
    ensure_directories()

    if not DATABASE_FILE.exists():
        return None

    backup_file = BACKUP_DIR / f"mission80_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    backup_file.write_bytes(DATABASE_FILE.read_bytes())
    return backup_file