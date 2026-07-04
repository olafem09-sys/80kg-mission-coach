import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from pathlib import Path

st.set_page_config(
    page_title="80kg Mission Coach",
    page_icon="💪",
    layout="wide"
)

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

EXERCISE_LIBRARY = {
    "Barbell Bench Press": {
        "category": "Push",
        "equipment": "Barbell, bench, plates",
        "muscles": "Chest, shoulders and triceps",
        "how": "Lie flat on the bench with your eyes under the bar. Grip slightly wider than shoulder width. Keep your feet planted, squeeze your shoulder blades together, lower the bar to mid-chest, then press up under control.",
        "mistakes": "Avoid bouncing the bar off your chest, lifting your hips, or flaring your elbows too wide.",
        "tip": "Use a weight that allows all reps with control. Stop 1–2 reps before failure while rebuilding the habit."
    },
    "Barbell Squat": {
        "category": "Legs",
        "equipment": "Barbell, plates",
        "muscles": "Quads, glutes, hamstrings and core",
        "how": "Stand with feet around shoulder-width apart. Brace your core, keep your chest up, sit the hips back and down, then drive through your heels to stand tall.",
        "mistakes": "Avoid knees collapsing inward, heels lifting, or rounding your back.",
        "tip": "Start lighter and focus on depth, control and balance."
    },
    "Romanian Deadlift": {
        "category": "Legs",
        "equipment": "Barbell or dumbbells",
        "muscles": "Hamstrings, glutes and lower back",
        "how": "Hold the bar or dumbbells in front of your thighs. Keep knees slightly bent, push your hips backwards, lower the weight close to your legs, then squeeze your glutes to return upright.",
        "mistakes": "Do not turn it into a squat. The movement should come mainly from the hips.",
        "tip": "You should feel a strong stretch in your hamstrings, not pain in your lower back."
    },
    "Walking Lunges": {
        "category": "Legs",
        "equipment": "Bodyweight or dumbbells",
        "muscles": "Quads, glutes, hamstrings and balance muscles",
        "how": "Step forward, lower until both knees are bent, then drive through the front heel to move into the next rep.",
        "mistakes": "Avoid leaning too far forward or taking very short steps.",
        "tip": "Keep your torso upright and take your time."
    },
    "Barbell Deadlift": {
        "category": "Full Body",
        "equipment": "Barbell, plates",
        "muscles": "Glutes, hamstrings, back, traps, grip and core",
        "how": "Stand with the bar over mid-foot. Hinge down, grip the bar, brace your core, keep the bar close, and push the floor away as you stand tall.",
        "mistakes": "Avoid rounding your back or letting the bar drift away from your body.",
        "tip": "Technique matters more than heavy weight, especially while returning to training."
    },
    "Barbell Bent-over Row": {
        "category": "Pull",
        "equipment": "Barbell, plates",
        "muscles": "Upper back, lats, rear shoulders and biceps",
        "how": "Hinge forward with a flat back. Pull the bar towards your lower ribs, squeeze your shoulder blades, then lower under control.",
        "mistakes": "Avoid jerking the weight or standing too upright.",
        "tip": "Keep your core tight and pull with your back, not just your arms."
    },
    "Dumbbell Shoulder Press": {
        "category": "Push",
        "equipment": "Dumbbells",
        "muscles": "Shoulders and triceps",
        "how": "Start with dumbbells at shoulder height. Brace your core and press overhead until your arms are almost straight, then lower slowly.",
        "mistakes": "Avoid arching your lower back or rushing the reps.",
        "tip": "Seated is easier to control; standing challenges your core more."
    },
    "Band Face Pull": {
        "category": "Pull",
        "equipment": "Resistance bands",
        "muscles": "Rear shoulders, upper back and rotator cuff",
        "how": "Anchor the band at face height. Pull towards your face with elbows high, pause, then return slowly.",
        "mistakes": "Avoid shrugging your shoulders or using momentum.",
        "tip": "Excellent for posture and shoulder health. Keep this in the plan."
    },
    "Goblet Squat": {
        "category": "Legs",
        "equipment": "Dumbbell or kettlebell",
        "muscles": "Quads, glutes and core",
        "how": "Hold one dumbbell close to your chest. Squat down under control, keep your elbows inside your knees, then stand tall.",
        "mistakes": "Avoid leaning forward excessively or letting your heels lift.",
        "tip": "Great for learning squat form safely."
    },
    "Plank": {
        "category": "Core",
        "equipment": "Bodyweight",
        "muscles": "Core, shoulders and glutes",
        "how": "Elbows under shoulders, body in a straight line, squeeze glutes and brace your abs. Breathe steadily.",
        "mistakes": "Avoid hips sagging or sticking too high.",
        "tip": "Quality matters more than duration."
    },
    "FitXR Combat": {
        "category": "Cardio",
        "equipment": "Oculus / Meta headset",
        "muscles": "Cardio system, shoulders, arms, core and legs",
        "how": "Choose a boxing or combat class. Keep your guard up, move your feet, punch with control and keep breathing.",
        "mistakes": "Avoid over-swinging your arms or stopping completely between combinations.",
        "tip": "Brilliant for fat loss because it feels more like a game than cardio."
    },
    "Treadmill Incline Walk": {
        "category": "Cardio",
        "equipment": "Treadmill",
        "muscles": "Cardio system, calves, glutes and legs",
        "how": "Walk briskly with a moderate incline. Keep posture tall and avoid holding the rails unless needed.",
        "mistakes": "Avoid setting the incline so high that your form collapses.",
        "tip": "Excellent low-impact fat-loss tool."
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

    done_dates = set(
        df[df["workout_done"].fillna(False).astype(bool)]["date"]
        .dropna()
        .astype(str)
    )

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
.stApp {
    background: #f4f7fb !important;
    color: #0f172a !important;
}

.block-container {
    padding-top: 1rem;
    max-width: 1450px;
}

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #0f172a;
}

.hero {
    background: linear-gradient(135deg, #111827, #1e3a8a, #7c3aed);
    padding: 34px;
    border-radius: 30px;
    color: white !important;
    margin-bottom: 24px;
    box-shadow: 0 14px 34px rgba(15,23,42,0.22);
}

.hero h1 {
    color: white !important;
    font-size: 42px;
    margin-bottom: 8px;
}

.hero p {
    color: #e0e7ff !important;
    font-size: 16px;
}

.card {
    background: #ffffff;
    padding: 22px;
    border-radius: 24px;
    box-shadow: 0 10px 28px rgba(15,23,42,0.08);
    border: 1px solid #e5e7eb;
    margin-bottom: 14px;
}

.metric-label {
    color: #64748b !important;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #0f172a !important;
    font-size: 31px;
    font-weight: 850;
}

.badge {
    display: inline-block;
    background: #eef2ff;
    color: #3730a3 !important;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 800;
    margin-bottom: 12px;
}

.exercise {
    background: #ffffff;
    padding: 13px 16px;
    border-radius: 14px;
    margin-bottom: 9px;
    border: 1px solid #dbeafe;
    color: #0f172a !important;
    box-shadow: 0 4px 12px rgba(15,23,42,0.04);
}

.coach-card {
    background: linear-gradient(135deg, #ecfeff, #eef2ff);
    border: 1px solid #c7d2fe;
}

.road-card {
    background: linear-gradient(135deg, #fff7ed, #ffedd5);
    border: 1px solid #fed7aa;
}

div[data-testid="stTabs"] button p {
    color: #0f172a !important;
    font-weight: 700;
}

div[data-testid="stTabs"] button[aria-selected="true"] p {
    color: #7c3aed !important;
}

.stProgress > div > div > div > div {
    background-color: #7c3aed;
}

@media only screen and (max-width: 768px) {
    .hero h1 {
        font-size: 30px;
    }

    .metric-value {
        font-size: 25px;
    }

    .card {
        padding: 18px;
    }
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
    <p>Garage gym training, FitXR cardio, Nigerian food coaching and your 95 kg → 80 kg transformation tracker.</p>
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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🏠 Dashboard",
    "💪 Today",
    "📝 Log",
    "📊 Charts",
    "🍛 Meal Coach",
    "🏆 Badges",
    "📚 Library",
    "🧠 Weekly Review",
    "🚗 Road Trip Mode"
])

with tab1:
    left, right = st.columns([1.35, 1])

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
        <div class="card coach-card">
            <h3>Daily Coach Score</h3>
            <div class="metric-value">{latest_score}/100</div>
            <p>Based on workout, water, protein, steps and energy.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>Coach Focus</h3>
            <p>Complete the session, log it, drink water and keep the streak alive.</p>
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

    st.info("Good form first, progress second. A completed session beats a perfect session skipped.")

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

    selected_category = st.selectbox(
        "Filter by category",
        ["All", "Push", "Pull", "Legs", "Full Body", "Cardio", "Core"]
    )

    for name, details in EXERCISE_LIBRARY.items():
        if selected_category != "All" and details["category"] != selected_category:
            continue

        with st.expander(name):
            st.write(f"**Category:** {details['category']}")
            st.write(f"**Equipment:** {details['equipment']}")
            st.write(f"**Muscles worked:** {details['muscles']}")
            st.write(f"**How to do it:** {details['how']}")
            st.write(f"**Common mistakes:** {details['mistakes']}")
            st.write(f"**Coach tip:** {details['tip']}")

with tab8:
    st.header("Weekly Coach Review")

    if df.empty:
        st.warning("No data yet. Log a few days first.")
    else:
        review_df = df.copy()
        review_df["date"] = pd.to_datetime(review_df["date"], errors="coerce")
        last_7 = review_df[review_df["date"] >= pd.Timestamp.today() - pd.Timedelta(days=7)]

        workouts_7 = int(last_7["workout_done"].fillna(False).astype(bool).sum())
        avg_steps = int(last_7["steps"].fillna(0).mean()) if not last_7.empty else 0
        avg_water = float(last_7["water_litres"].fillna(0).mean()) if not last_7.empty else 0
        avg_score = int(last_7["daily_score"].fillna(0).mean()) if not last_7.empty else 0
        fitxr_total = int(last_7["fitxr_calories"].fillna(0).sum()) if not last_7.empty else 0

        a, b, c, d = st.columns(4)
        a.metric("Workouts", workouts_7)
        b.metric("Avg Steps", avg_steps)
        c.metric("Avg Water", f"{avg_water:.1f} L")
        d.metric("Avg Score", f"{avg_score}/100")

        st.metric("FitXR Calories This Week", fitxr_total)

        st.subheader("Coach Feedback")

        if workouts_7 >= 4:
            st.success("Strong training week. You are building real consistency.")
        elif workouts_7 >= 2:
            st.warning("Decent week, but push towards 4+ sessions.")
        else:
            st.error("Low activity week. Next week, focus on simply showing up.")

        if avg_water >= 2.5:
            st.success("Hydration is on target.")
        else:
            st.warning("Hydration needs work. Aim for 2.5 litres daily.")

        if avg_steps >= 8000:
            st.success("Steps are strong.")
        else:
            st.warning("Try to increase your daily steps gradually.")

with tab9:
    st.header("Road Trip Mode 🚗")

    st.markdown("""
    <div class="card road-card">
        <h3>Travel Training Plan</h3>
        <p>This is for your July road trip. The aim is not perfection — it is to avoid losing momentum.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Minimum Travel Workout — 15 minutes")
    travel_items = [
        "Bodyweight Squats — 3 × 15",
        "Press-ups or incline press-ups — 3 × 10",
        "Walking Lunges — 3 × 10 each leg",
        "Plank — 3 × 30 seconds",
        "Brisk walk — 10–20 minutes"
    ]

    for item in travel_items:
        st.markdown(f"<div class='exercise'>{item}</div>", unsafe_allow_html=True)

    st.info("Road trip rule: even 15 minutes keeps the identity alive. Do not aim for perfect — aim for consistent.")
