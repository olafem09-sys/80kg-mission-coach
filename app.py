from datetime import datetime

import streamlit as st

from components.navigation import sidebar_navigation
from components.styles import apply_global_styles
from config import APP_NAME
from pages import coach, dashboard, exercise_library, nutrition, progress, settings, workout
from utils.storage import get_user_profile, initialise_database

st.set_page_config(page_title=APP_NAME, page_icon="💪", layout="wide")

initialise_database()
apply_global_styles()

profile = get_user_profile()
today = datetime.now().strftime("%A")
page = sidebar_navigation()

if page == "Dashboard":
    dashboard.render(profile, today)

elif page == "Workout":
    workout.render(today)

elif page == "Exercise Library":
    exercise_library.render()

elif page == "Nutrition":
    nutrition.render()

elif page == "Progress":
    progress.render()

elif page == "AI Coach":
    coach.render()

elif page == "Settings":
    settings.render(profile)