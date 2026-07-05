"""
Mission 80 Coach
Nutrition Page
"""

import pandas as pd
import streamlit as st

from components.styles import content_card, hero
from utils.storage import get_food_database


def render() -> None:
    """Render Nutrition Centre page."""

    hero(
        "Nutrition Centre 🍽",
        "Select foods, build meal plans and stay aligned with your 80 kg goal.",
    )

    foods = pd.DataFrame(get_food_database())

    content_card(
        "Nutrition Focus",
        "Prioritise protein, control portions, keep Nigerian meals realistic, and aim for 2.5 litres of water daily.",
        badge="Food Coach",
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Food List",
            "Meal Timetable",
            "Meal Recommendation",
        ]
    )

    with tab1:
        st.subheader("Food Database")

        if foods.empty:
            st.warning("No foods found in the database.")
            return

        cuisine = st.selectbox(
            "Cuisine",
            ["All"] + sorted(foods["cuisine"].dropna().unique().tolist()),
        )

        category = st.selectbox(
            "Category",
            ["All"] + sorted(foods["category"].dropna().unique().tolist()),
        )

        filtered = foods.copy()

        if cuisine != "All":
            filtered = filtered[filtered["cuisine"] == cuisine]

        if category != "All":
            filtered = filtered[filtered["category"] == category]

        st.dataframe(
            filtered[
                [
                    "food_name",
                    "category",
                    "cuisine",
                    "portion_description",
                    "calories",
                    "protein_g",
                    "carbs_g",
                    "fat_g",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    with tab2:
        st.subheader("Example Daily Food Timetable")

        st.markdown(
            """
            **Breakfast**  
            Eggs + soda bread + tea

            **Lunch**  
            Rice and stew + grilled chicken or fish

            **Snack**  
            Greek yoghurt, fruit or boiled eggs

            **Dinner**  
            Moi Moi, beans, grilled fish, chicken, or a controlled rice portion
            """
        )

        st.info(
            "This is the first meal timetable shell. In the Nutrition sprint, this will become selectable and customisable."
        )

    with tab3:
        st.subheader("Food Recommendation")

        goal = st.selectbox(
            "What do you need?",
            [
                "High protein meal",
                "Lower calorie meal",
                "Training day meal",
                "Rest day meal",
                "Nigerian meal option",
            ],
        )

        if goal == "High protein meal":
            st.success("Recommended: eggs, grilled chicken, grilled fish, beans, Moi Moi or Greek yoghurt.")

        elif goal == "Lower calorie meal":
            st.success("Recommended: grilled fish or chicken with controlled rice portion and stew with less oil.")

        elif goal == "Training day meal":
            st.success("Recommended: rice and stew with chicken or fish. Keep rice moderate and protein high.")

        elif goal == "Rest day meal":
            st.success("Recommended: Moi Moi, beans, fish, eggs or chicken with a smaller carb portion.")

        elif goal == "Nigerian meal option":
            st.success("Recommended: rice and stew, beans, Moi Moi, pepper soup, grilled fish, or Efo Riro with controlled swallow/rice.")