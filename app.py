from datetime import datetime

import pandas as pd
import streamlit as st

from components.navigation import sidebar_navigation
from components.styles import apply_global_styles, hero, exercise_row, content_card
from components.cards import stat_card, milestone_card
from config import APP_NAME, START_WEIGHT, TARGET_WEIGHT
from utils.storage import (
    get_food_database,
    get_recent_workouts,
    get_user_profile,
    initialise_database,
)
from utils.workout_data import (
    get_today_workout,
    get_exercises_by_category,
    get_exercise_names,
)

st.set_page_config(page_title=APP_NAME, page_icon="💪", layout="wide")

initialise_database()
apply_global_styles()

profile = get_user_profile()
page = sidebar_navigation()

today = datetime.now().strftime("%A")
today_workout = get_today_workout(today)

weight_now = profile["start_weight_kg"] if profile else START_WEIGHT
target_weight = profile["target_weight_kg"] if profile else TARGET_WEIGHT
remaining = max(0, weight_now - target_weight)
progress = max(0, min(100, (START_WEIGHT - weight_now) / (START_WEIGHT - TARGET_WEIGHT) * 100))


if page == "Dashboard":
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


elif page == "Workout":
    hero("Workout Centre 💪", "Track today’s planned workout and add extra exercises.")

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
        st.success("Workout captured. Full database save will be connected in the Workout Centre sprint.")

        st.write("**Completed planned exercises:**", completed)
        st.write("**Extra exercises:**", extra)

        if manual:
            st.write("**Manual exercise:**", manual)

        st.write("**Duration:**", duration)
        st.write("**FitXR:**", f"{fitxr_minutes} mins · {fitxr_calories} calories")

        if notes:
            st.write("**Notes:**", notes)


elif page == "Exercise Library":
    hero("Exercise Library 📚", "Search exercises by category, muscle or equipment.")

    category = st.selectbox(
        "Category",
        ["All", "Push", "Pull", "Legs", "Full Body", "Core", "Cardio", "Mobility", "Recovery"],
    )

    search = st.text_input("Search")

    exercises = get_exercises_by_category(category)

    if search:
        term = search.lower()
        exercises = {
            name: details
            for name, details in exercises.items()
            if term in name.lower()
            or term in " ".join(details["equipment"]).lower()
            or term in " ".join(details["muscles"]).lower()
        }

    for name, details in exercises.items():
        with st.expander(name):
            st.write(f"**Category:** {details['category']}")
            st.write(f"**Equipment:** {', '.join(details['equipment'])}")
            st.write(f"**Muscles:** {', '.join(details['muscles'])}")
            st.write(f"**Difficulty:** {details['difficulty']}")

            if details.get("video"):
                st.info("Video slot ready. Add matching MP4 files into assets/videos.")

            st.write(f"**Instructions:** {details['instructions']}")
            st.write(f"**Common mistakes:** {details['common_mistakes']}")
            st.write(f"**Coach tip:** {details['coach_tip']}")
            st.write(f"**Alternatives:** {', '.join(details['alternatives'])}")


elif page == "Nutrition":
    hero("Nutrition Centre 🍽", "Food list, Nigerian meals and meal timetable planning.")

    foods = pd.DataFrame(get_food_database())

    content_card(
        "Nutrition Goal",
        "Build meals around protein, controlled carbohydrates, water and realistic Nigerian food choices.",
        badge="Food Coach",
    )

    if not foods.empty:
        cuisine = st.selectbox("Cuisine", ["All"] + sorted(foods["cuisine"].unique().tolist()))

        filtered = foods.copy()
        if cuisine != "All":
            filtered = filtered[filtered["cuisine"] == cuisine]

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

    st.subheader("Example Food Timetable")

    st.markdown(
        """
        **Breakfast:** Eggs + soda bread + tea  
        **Lunch:** Rice and stew + grilled chicken or fish  
        **Snack:** Greek yoghurt, fruit or boiled eggs  
        **Dinner:** Moi Moi, beans, fish, chicken or controlled rice portion  
        """
    )


elif page == "Progress":
    hero("Progress Centre 📈", "Track weight, measurements and long-term progress.")

    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card("Start Weight", f"{START_WEIGHT:.1f} kg")
    with c2:
        stat_card("Target Weight", f"{TARGET_WEIGHT:.1f} kg")
    with c3:
        stat_card("Total Goal", f"{START_WEIGHT - TARGET_WEIGHT:.1f} kg loss")

    content_card(
        "Progress Tracking",
        "Weight logs, measurements, progress photos and trend charts will be added here.",
        badge="Progress",
    )


elif page == "AI Coach":
    hero("AI Coach 🤖", "Personalised coaching based on training, nutrition and habits.")

    content_card(
        "Today’s Coaching",
        "Complete the planned session if possible. If time is limited, choose the minimum effective session: 20 minutes.",
        badge="Daily Coach",
    )

    content_card(
        "Nutrition Advice",
        "Keep protein high today. If eating rice and stew, control the rice portion and prioritise meat, fish, eggs or beans.",
        badge="Meal Coach",
    )

    content_card(
        "Next Build",
        "The AI Coach will become more intelligent once workout, nutrition and progress logs are fully connected.",
        badge="Coming Soon",
    )


elif page == "Settings":
    hero("Settings ⚙️", "Profile, targets and app preferences.")

    st.subheader("User Profile")

    if profile:
        st.json(dict(profile))
    else:
        st.warning("No profile found.")

    st.info("Editable settings will be added after the database write functions are connected.")