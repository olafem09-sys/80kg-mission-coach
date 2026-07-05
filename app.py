from datetime import datetime

import pandas as pd
import streamlit as st

from components.styles import (
    apply_global_styles,
    content_card,
    exercise_row,
    hero,
    metric_card,
)
from config import APP_NAME, START_WEIGHT, TARGET_WEIGHT
from utils.storage import (
    get_food_database,
    get_recent_workouts,
    get_user_profile,
    initialise_database,
)
from utils.workout_data import (
    EXERCISE_LIBRARY,
    get_exercise_names,
    get_exercises_by_category,
    get_today_workout,
)

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💪",
    layout="wide",
)

initialise_database()
apply_global_styles()

profile = get_user_profile()
today_name = datetime.now().strftime("%A")
today_workout = get_today_workout(today_name)

hero(
    "Mission 80 Coach 💪",
    "Your personalised training, nutrition and lifestyle coaching dashboard.",
)

current_weight = profile["start_weight_kg"] if profile else START_WEIGHT
target_weight = profile["target_weight_kg"] if profile else TARGET_WEIGHT
weight_to_lose = max(0, current_weight - target_weight)
progress = max(0, min(100, ((START_WEIGHT - current_weight) / (START_WEIGHT - TARGET_WEIGHT)) * 100))

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Current Weight", f"{current_weight:.1f} kg", "Starting point for Mission 80")

with col2:
    metric_card("Target Weight", f"{target_weight:.1f} kg", "Main transformation goal")

with col3:
    metric_card("To Lose", f"{weight_to_lose:.1f} kg", "Remaining journey")

with col4:
    metric_card("Today", today_name, today_workout["title"])

st.progress(progress / 100)
st.caption(f"Mission progress: {progress:.1f}% complete")

tabs = st.tabs(
    [
        "🏠 Dashboard",
        "💪 Today",
        "📚 Exercise Library",
        "🍽 Nutrition",
        "📈 Progress",
        "🤖 Coach",
        "⚙️ Settings",
    ]
)

with tabs[0]:
    left, right = st.columns([1.4, 1])

    with left:
        content_card(
            "Today’s Focus",
            f"{today_workout['focus']} · Expected duration: {today_workout['duration']}",
            badge=today_workout["title"],
        )

        st.subheader("Today’s Plan")
        for exercise in today_workout["exercises"]:
            exercise_row(exercise, "Planned exercise")

    with right:
        content_card(
            "Coach Message",
            "Do the planned session if possible. If time is tight, complete at least 20 minutes. Consistency beats perfection.",
            badge="Daily Coach",
        )

        content_card(
            "Nutrition Focus",
            "Protein first today. Keep rice portions controlled and aim for 2.5 litres of water.",
            badge="Meal Guidance",
        )

with tabs[1]:
    st.header(f"{today_name}: {today_workout['title']}")

    st.write(today_workout["focus"])

    completed = []
    for exercise in today_workout["exercises"]:
        if st.checkbox(exercise):
            completed.append(exercise)

    st.subheader("Add Extra Exercise")

    exercise_options = get_exercise_names()
    extra_selected = st.multiselect(
        "Select extra exercises completed today",
        exercise_options,
    )

    manual_extra = st.text_input("Manual exercise entry, if not listed")

    if st.button("Save Workout Summary"):
        st.success("Workout summary captured for this session. Full database logging will be added in the Workout Centre sprint.")

        st.write("**Completed planned exercises:**")
        st.write(completed if completed else "None selected")

        st.write("**Extra exercises:**")
        st.write(extra_selected if extra_selected else "None selected")

        if manual_extra:
            st.write("**Manual entry:**")
            st.write(manual_extra)

with tabs[2]:
    st.header("Garage Gym Exercise Library")

    category = st.selectbox(
        "Filter by category",
        ["All", "Push", "Pull", "Legs", "Full Body", "Core", "Cardio", "Mobility", "Recovery"],
    )

    search = st.text_input("Search exercises")

    exercises = get_exercises_by_category(category)

    if search:
        exercises = {
            name: details
            for name, details in exercises.items()
            if search.lower() in name.lower()
            or search.lower() in " ".join(details["muscles"]).lower()
            or search.lower() in " ".join(details["equipment"]).lower()
        }

    for name, details in exercises.items():
        with st.expander(name):
            st.write(f"**Category:** {details['category']}")
            st.write(f"**Equipment:** {', '.join(details['equipment'])}")
            st.write(f"**Muscles:** {', '.join(details['muscles'])}")
            st.write(f"**Difficulty:** {details['difficulty']}")

            if details.get("video"):
                st.info("Local demo video slot ready. Add MP4 files into assets/videos to enable playback.")

            st.write(f"**Instructions:** {details['instructions']}")
            st.write(f"**Common mistakes:** {details['common_mistakes']}")
            st.write(f"**Coach tip:** {details['coach_tip']}")
            st.write(f"**Alternatives:** {', '.join(details['alternatives'])}")

with tabs[3]:
    st.header("Nutrition Centre")

    food_data = get_food_database()
    food_df = pd.DataFrame(food_data)

    content_card(
        "Nutrition Goal",
        "Build meals around protein, controlled carbs, water and realistic Nigerian food choices.",
        badge="Food Coach",
    )

    if not food_df.empty:
        cuisine_filter = st.selectbox(
            "Cuisine",
            ["All"] + sorted(food_df["cuisine"].dropna().unique().tolist()),
        )

        filtered_df = food_df.copy()

        if cuisine_filter != "All":
            filtered_df = filtered_df[filtered_df["cuisine"] == cuisine_filter]

        st.dataframe(
            filtered_df[
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

with tabs[4]:
    st.header("Progress Centre")

    content_card(
        "Progress Tracking",
        "Weight, measurements, photos and trend charts will be added here in the Progress sprint.",
        badge="Coming in Sprint",
    )

    st.write("Initial target:")
    st.write(f"- Start weight: {START_WEIGHT} kg")
    st.write(f"- Target weight: {TARGET_WEIGHT} kg")
    st.write(f"- Total goal: {START_WEIGHT - TARGET_WEIGHT:.1f} kg loss")

with tabs[5]:
    st.header("AI Coach")

    content_card(
        "Daily Coaching",
        "Your AI coach will use workouts, meals, sleep, mood, water, steps and progress data to produce daily recommendations.",
        badge="Coach Engine",
    )

    st.info(
        "For now, this page shows the shell. The full AI Coach logic will be added after the Workout, Nutrition and Progress modules are connected."
    )

with tabs[6]:
    st.header("Settings")

    st.write("Profile loaded from SQLite:")

    if profile:
        st.json(dict(profile))
    else:
        st.warning("No profile found.")

    st.write("Settings editing will be added in the Settings sprint.")