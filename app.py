import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from pathlib import Path

st.set_page_config(page_title="80kg Mission Coach", page_icon="💪", layout="wide")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
LOG_FILE = DATA_DIR / "fitness_log.csv"

START_WEIGHT = 95.0
TARGET_WEIGHT = 80.0
JULY_WORKOUT_TARGET = 20

LOG_COLUMNS = [
    "date", "weight", "workout_done", "workout_type",
    "fitxr_minutes", "fitxr_calories", "steps",
    "water_litres", "protein_grams", "energy",
    "meal_score", "daily_score", "notes"
]

WORKOUTS = {
    "Monday": {
        "title": "Upper Body + Core",
        "focus": "Chest, shoulders, triceps and core",
        "duration": "45–60 mins",
        "items": [
            "Barbell Bench Press — 4 × 8",
            "Standing Shoulder Press — 4 × 8",
            "Incline Dumbbell Press — 3 × 10",
            "Band Triceps Pushdown — 3 × 15",
            "Plank — 3 × 45 sec",
            "Treadmill Walk — 10 mins"
        ]
    },
    "Tuesday": {
        "title": "FitXR Cardio",
        "focus": "Fat burn and conditioning",
        "duration": "30–45 mins",
        "items": [
            "FitXR Combat / Boxing — 30–45 mins",
            "Kettlebell Swings — 3 × 20",
            "Stretch — 5 mins"
        ]
    },
    "Wednesday": {
        "title": "Lower Body",
        "focus": "Legs, glutes and core",
        "duration": "45–60 mins",
        "items": [
            "Barbell Squat — 4 × 8",
            "Romanian Deadlift — 4 × 10",
            "Walking Lunges — 3 × 12 each leg",
            "Band Glute Kickback — 3 × 15 each leg",
            "Calf Raises — 4 × 15",
            "Plank — 3 × 45 sec"
        ]
    },
    "Thursday": {
        "title": "Recovery Walk + Mobility",
        "focus": "Recovery and movement",
        "duration": "30–45 mins",
        "items": [
            "Treadmill Walk — 30–40 mins",
            "Hip Flexor Stretch — 30 sec each side",
            "Hamstring Stretch — 30 sec each side",
            "Child’s Pose — 60 sec",
            "Shoulder Circles — 20 reps"
        ]
    },
    "Friday": {
        "title": "Full Body Strength",
        "focus": "Strength and muscle retention",
        "duration": "45–60 mins",
        "items": [
            "Barbell Deadlift — 4 × 6",
            "Barbell Bench Press — 4 × 8",
            "Barbell Bent-over Row — 4 × 8",
            "Dumbbell Shoulder Press — 3 × 10",
            "Goblet Squat — 3 × 12",
            "Band Face Pulls — 3 × 15"
        ]
    },
    "Saturday": {
        "title": "FitXR Cardio",
        "focus": "Fun cardio and calorie burn",
        "duration": "45–60 mins",
        "items": [
            "FitXR Combat / Boxing — 45–60 mins",
            "Optional Incline Treadmill Walk — 10 mins",
            "Stretch — 5 mins"
        ]
    },
    "Sunday": {
        "title": "Rest Day",
        "focus": "Recovery and weekly review",
        "duration": "Optional",
        "items": [
            "Rest",
            "Light walk if desired",
            "Weekly weigh-in review",
            "Prepare for next week"
        ]
    }
}

ACHIEVEMENTS = [
    ("🔥", "First Workout", "Complete your first logged workout.", lambda w, wt: w >= 1),
    ("💪", "5 Workout Club", "Complete 5 workouts.", lambda w, wt: w >= 5),
    ("🏋️", "10 Workout Club", "Complete 10 workouts.", lambda w, wt: w >= 10),
    ("🥉", "92kg Club", "Reach 92 kg or below.", lambda w, wt: wt <= 92),
    ("🥈", "90kg Club", "Reach 90 kg or below.", lambda w, wt: wt <= 90),
    ("🥇", "85kg Club", "Reach 85 kg or below.", lambda w, wt: wt <= 85),
    ("🏆", "Mission Complete", "Reach your 80 kg target.", lambda w, wt: wt <= 80),
]

EXERCISE_LIBRARY = {
    "Barbell Bench Press": ["Push", "Barbell, bench, plates", "Lower to mid-chest and press up under control."],
    "Barbell Squat": ["Legs", "Barbell, plates", "Brace core, squat down under control, drive back up."],
    "Romanian Deadlift": ["Legs", "Barbell or dumbbells", "Hinge at the hips and feel the stretch in your hamstrings."],
    "Walking Lunges": ["Legs", "Dumbbells optional", "Step forward, lower under control, drive through front heel."],
    "Barbell Deadlift": ["Full Body", "Barbell, plates", "Bar close to body, brace, drive through the floor."],
    "Barbell Bent-over Row": ["Pull", "Barbell, plates", "Hinge forward and pull towards lower ribs."],
    "Dumbbell Shoulder Press": ["Push", "Dumbbells", "Press overhead while bracing your core."],
    "Band Face Pull": ["Pull", "Resistance bands", "Pull band towards your face with elbows high."],
    "FitXR Combat": ["Cardio", "Oculus / Meta headset", "Keep moving and maintain good punching form."],
    "Treadmill Incline Walk": ["Cardio", "Treadmill", "Brisk walk with incline; breathing harder but still controlled."]
}


def load_log():
    if not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=LOG_COLUMNS)
    try:
        df = pd.read_csv(LOG_FILE)
        for col in LOG_COLUMNS:
            if col not in df.columns:
                df[col] = None
        return df[LOG_COLUMNS]
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=LOG_COLUMNS)


def save_log(entry):
    df = load_log()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)


def latest_weight(df):
    if df.empty or df["weight"].dropna().empty:
        return START_WEIGHT
    return float(df["weight"].dropna().iloc[-1])


def workout_count(df):
    if df.empty:
        return 0
    return int(df["workout_done"].fillna(False).astype(bool).sum())


def current_streak(df):
    if df.empty:
        return 0
    done_dates = set(df[df["workout_done"].fillna(False).astype(bool)]["date"].dropna().astype(str))
    streak = 0
    current = date.today()
    while current.isoformat() in done_dates:
        streak += 1
        current = current - pd.Timedelta(days=1)
    return streak


def daily_score(workout_done, water, protein, steps, energy):
    score = 0
    score += 30 if workout_done else 0
    score += 20 if water >= 2.5 else 10 if water >= 1.5 else 0
    score += 20 if protein >= 140 else 10 if protein >= 100 else 0
    score += 20 if steps >= 8000 else 10 if steps >= 5000 else 0
    score += 10 if energy >= 7 else 5 if energy >= 5 else 0
    return score


def meal_colour(score):
    if score >= 9:
        return "🟢 Green"
    if score >= 7:
        return "🟡 Amber"
    return "🔴 Red"


st.markdown("""
<style>
.block-container { padding-top: 1rem; }
.hero {
    background: linear-gradient(135deg, #111827, #1e3a8a, #7c3aed);
    padding: 32px;
    border-radius: 30px;
    color: white;
    margin-bottom: 25px;
}
.hero h1, .hero p { color: white !important; }
.card {
    background: white;
    padding: 22px;
    border-radius: 24px;
    box-shadow: 0 10px 30px rgba(15,23,42,0.08);
    border: 1px solid #e5e7eb;
    margin-bottom: 14px;
}
.metric-label { color: #64748b; font-size: 14px; }
.metric-value { color: #0f172a; font-size: 32px; font-weight: 800; }
.badge {
    display: inline-block;
    background: #eef2ff;
    color: #3730a3;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 700;
    margin-bottom: 10px;
}
.exercise {
    background: #f8fafc;
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 8px;
    border: 1px solid #e2e8f0;
    color: #0f172a;
}
.stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label {
    color: #0f172a !important;
}
[data-testid="stTabs"] p {
    color: inherit !important;
}
</style>
""", unsafe_allow_html=True)

df = load_log()
today = datetime.now().strftime("%A")
today_workout = WORKOUTS[today]

weight_now = latest_weight(df)
lost = START_WEIGHT - weight_now
remaining = max(0, weight_now - TARGET_WEIGHT)
progress = max(0, min(100, (lost / (START_WEIGHT - TARGET_WEIGHT)) * 100))
completed = workout_count(df)
streak = current_streak(df)

latest_score = 0
if not df.empty and df["daily_score"].notna().any():
    latest_score = int(float(df["daily_score"].dropna().iloc[-1]))

st.markdown("""
<div class="hero">
    <h1>80kg Mission Coach 💪</h1>
    <p>Personalised coaching dashboard: garage gym, FitXR, Nigerian food, fat loss and consistency.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='card'><div class='metric-label'>Current Weight</div><div class='metric-value'>{weight_now:.1f} kg</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='card'><div class='metric-label'>Weight Lost</div><div class='metric-value'>{lost:.1f} kg</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='card'><div class='metric-label'>July Workouts</div><div class='metric-value'>{completed}/{JULY_WORKOUT_TARGET}</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='card'><div class='metric-label'>Current Streak</div><div class='metric-value'>{streak} days</div></div>", unsafe_allow_html=True)

st.progress(progress / 100)
st.caption(f"Mission progress: {progress:.1f}% complete — {remaining:.1f} kg left to reach 80 kg.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Dashboard",
    "💪 Today’s Workout",
    "📝 Log Progress",
    "📊 Charts",
    "🍛 Meal Coach",
    "🏆 Achievements",
    "📚 Exercise Library"
])

with tab1:
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown(f"""
        <div class="card">
            <span class="badge">{today}</span>
            <h2>{today_workout['title']}</h2>
            <p><b>Focus:</b> {today_workout['focus']}</p>
            <p><b>Expected duration:</b> {today_workout['duration']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Today’s Plan")
        for item in today_workout["items"]:
            st.markdown(f"<div class='exercise'>{item}</div>", unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="card">
            <h3>Daily Coach Score</h3>
            <div class="metric-value">{latest_score}/100</div>
            <p>Based on workout, water, protein, steps and energy.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>Coach Focus</h3>
            <p>Do not chase perfection. Complete the session, log it, drink water, and keep the streak alive.</p>
            <p><b>Minimum today:</b> 20 minutes still counts.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>Milestones</h3>
            <p>🥉 92 kg Club</p>
            <p>🥈 90 kg Club</p>
            <p>🥇 85 kg Club</p>
            <p>🏆 80 kg Mission Complete</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.header(f"{today}: {today_workout['title']}")
    st.write(today_workout["focus"])
    for item in today_workout["items"]:
        st.checkbox(item)
    st.info("Coach note: good form first, progress second.")

with tab3:
    st.header("Log Today’s Progress")

    with st.form("log_form"):
        log_date = st.date_input("Date", value=date.today())
        weight = st.number_input("Weight, kg", 60.0, 150.0, value=weight_now, step=0.1)
        workout_done = st.checkbox("Workout completed?")
        workout_type = st.selectbox("Workout type", ["Strength", "Cardio", "Recovery", "Rest", "Mixed"])
        fitxr_minutes = st.number_input("FitXR minutes", 0, 180, value=0)
        fitxr_calories = st.number_input("FitXR calories", 0, 2000, value=0)
        steps = st.number_input("Steps", 0, 50000, value=0)
        water = st.number_input("Water, litres", 0.0, 6.0, value=0.0, step=0.1)
        protein = st.number_input("Protein, grams", 0, 300, value=0)
        energy = st.slider("Energy level", 1, 10, 5)
        meal_score = st.slider("Meal score today", 1, 10, 8)
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Progress")

        if submitted:
            score_today = daily_score(workout_done, water, protein, steps, energy)

            save_log({
                "date": log_date.isoformat(),
                "weight": weight,
                "workout_done": workout_done,
                "workout_type": workout_type,
                "fitxr_minutes": fitxr_minutes,
                "fitxr_calories": fitxr_calories,
                "steps": steps,
                "water_litres": water,
                "protein_grams": protein,
                "energy": energy,
                "meal_score": meal_score,
                "daily_score": score_today,
                "notes": notes
            })

            st.success(f"Saved. Daily Coach Score: {score_today}/100")
            st.rerun()

with tab4:
    st.header("Progress Charts")

    if df.empty:
        st.warning("No logs yet. Add your first entry.")
    else:
        chart_df = df.copy()
        chart_df["date"] = pd.to_datetime(chart_df["date"], errors="coerce")

        fig_weight = px.line(chart_df, x="date", y="weight", markers=True, title="Weight Progress")
        fig_weight.add_hline(y=TARGET_WEIGHT, line_dash="dash", annotation_text="80 kg target")
        st.plotly_chart(fig_weight, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(px.bar(chart_df, x="date", y="steps", title="Steps"), use_container_width=True)
        with col_b:
            st.plotly_chart(px.bar(chart_df, x="date", y="fitxr_calories", title="FitXR Calories"), use_container_width=True)

        if "daily_score" in chart_df.columns:
            fig_score = px.line(chart_df, x="date", y="daily_score", markers=True, title="Daily Coach Score")
            fig_score.add_hline(y=85, line_dash="dash", annotation_text="Elite Day")
            st.plotly_chart(fig_score, use_container_width=True)

        st.dataframe(chart_df.sort_values("date", ascending=False), use_container_width=True)

with tab5:
    st.header("Meal Coach")
    score = st.slider("Meal score", 1, 10, 8)
    st.metric("Meal Category", meal_colour(score))
    meal = st.text_area("Describe the meal")

    if st.button("Get Coach Feedback"):
        if score >= 9:
            st.success("Green meal. Keep it in your regular rotation.")
        elif score >= 7:
            st.warning("Amber meal. Good, but improve one thing: portion, oil, sugar or protein.")
        else:
            st.error("Red meal. Enjoy occasionally, but do not make it a daily habit.")

        st.write("For Nigerian meals:")
        st.write("- Protein first: eggs, fish, chicken, turkey, beans or lean beef.")
        st.write("- Rice portion: about one fist-sized serving.")
        st.write("- Stew: flavour is fine, but watch excess oil.")
        st.write("- Water: aim for 2.5–3 litres daily.")

with tab6:
    st.header("Achievement Badges")

    cols = st.columns(3)
    for i, (emoji, name, desc, condition) in enumerate(ACHIEVEMENTS):
        unlocked = condition(completed, weight_now)
        with cols[i % 3]:
            if unlocked:
                st.success(f"{emoji} **{name}**\n\n{desc}")
            else:
                st.info(f"🔒 **{name}**\n\n{desc}")

with tab7:
    st.header("Garage Gym Exercise Library")

    selected_category = st.selectbox("Filter by category", ["All", "Push", "Pull", "Legs", "Full Body", "Cardio"])

    for name, details in EXERCISE_LIBRARY.items():
        category, equipment, how = details

        if selected_category != "All" and category != selected_category:
            continue

        with st.expander(name):
            st.write(f"**Category:** {category}")
            st.write(f"**Equipment:** {equipment}")
            st.write(f"**How to do it:** {how}")
