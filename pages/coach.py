"""
Mission 80 Coach
AI Coach Page
"""

from components.styles import content_card, hero


def render() -> None:
    """Render AI Coach page."""

    hero(
        "AI Coach 🤖",
        "Personalised coaching based on your workouts, nutrition and progress.",
    )

    content_card(
        "Today’s Coaching",
        "Complete the planned session if possible. If time is limited, complete at least 20 minutes.",
        badge="Daily Coach",
    )

    content_card(
        "Nutrition Advice",
        "Keep protein high today. If eating rice and stew, control the rice portion and prioritise meat, fish, eggs or beans.",
        badge="Meal Coach",
    )

    content_card(
        "Next Step",
        "The coach will become more intelligent once workout, nutrition and progress logs are fully connected.",
        badge="Coach Engine",
    )