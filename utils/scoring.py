"""
Mission 80 Coach
Daily Coach Scoring Engine
Version 2.0
"""

from dataclasses import dataclass


@dataclass
class DailyMetrics:
    workout_completed: bool
    workout_minutes: int
    water_litres: float
    protein_grams: float
    steps: int
    sleep_hours: float
    mood_score: int


def calculate_score(metrics: DailyMetrics) -> dict:
    """
    Returns:
        score (0-100)
        breakdown
        coach_message
    """

    score = 0

    breakdown = {
        "Workout": 0,
        "Water": 0,
        "Protein": 0,
        "Steps": 0,
        "Sleep": 0,
        "Mood": 0,
    }

    # -----------------------
    # Workout (30)
    # -----------------------

    if metrics.workout_completed:
        breakdown["Workout"] = 20

        if metrics.workout_minutes >= 45:
            breakdown["Workout"] += 10
        elif metrics.workout_minutes >= 30:
            breakdown["Workout"] += 6
        elif metrics.workout_minutes >= 20:
            breakdown["Workout"] += 4

    # -----------------------
    # Water (15)
    # -----------------------

    if metrics.water_litres >= 2.5:
        breakdown["Water"] = 15
    elif metrics.water_litres >= 2:
        breakdown["Water"] = 12
    elif metrics.water_litres >= 1.5:
        breakdown["Water"] = 8

    # -----------------------
    # Protein (20)
    # -----------------------

    if metrics.protein_grams >= 170:
        breakdown["Protein"] = 20
    elif metrics.protein_grams >= 140:
        breakdown["Protein"] = 16
    elif metrics.protein_grams >= 100:
        breakdown["Protein"] = 12
    elif metrics.protein_grams >= 70:
        breakdown["Protein"] = 8

    # -----------------------
    # Steps (15)
    # -----------------------

    if metrics.steps >= 10000:
        breakdown["Steps"] = 15
    elif metrics.steps >= 8000:
        breakdown["Steps"] = 12
    elif metrics.steps >= 6000:
        breakdown["Steps"] = 8
    elif metrics.steps >= 4000:
        breakdown["Steps"] = 4

    # -----------------------
    # Sleep (10)
    # -----------------------

    if metrics.sleep_hours >= 8:
        breakdown["Sleep"] = 10
    elif metrics.sleep_hours >= 7:
        breakdown["Sleep"] = 8
    elif metrics.sleep_hours >= 6:
        breakdown["Sleep"] = 5

    # -----------------------
    # Mood (10)
    # -----------------------

    breakdown["Mood"] = max(0, min(metrics.mood_score, 10))

    score = sum(breakdown.values())

    # -----------------------
    # Coach feedback
    # -----------------------

    if score >= 90:
        message = "Outstanding day. You're building excellent habits."
    elif score >= 75:
        message = "Strong day. Stay consistent."
    elif score >= 60:
        message = "Good progress. A little more effort tomorrow."
    elif score >= 40:
        message = "You showed up. Let's improve one habit tomorrow."
    else:
        message = "Tomorrow is a fresh start. Focus on one small win."

    return {
        "score": score,
        "breakdown": breakdown,
        "message": message,
    }