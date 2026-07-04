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
    {
        "name": "First Workout",
        "emoji": "🔥",
        "description": "Completed your first logged workout.",
        "condition": "workouts >= 1"
    },
    {
        "name": "5 Workout Club",
        "emoji": "💪",
        "description": "Completed 5 workouts.",
        "condition": "workouts >= 5"
    },
    {
        "name": "10 Workout Club",
        "emoji": "🏋️",
        "description": "Completed 10 workouts.",
        "condition": "workouts >= 10"
    },
    {
        "name": "92kg Club",
        "emoji": "🥉",
        "description": "Reached 92 kg or below.",
        "condition": "weight <= 92"
    },
    {
        "name": "90kg Club",
        "emoji": "🥈",
        "description": "Reached 90 kg or below.",
        "condition": "weight <= 90"
    },
    {
        "name": "85kg Club",
        "emoji": "🥇",
        "description": "Reached 85 kg or below.",
        "condition": "weight <= 85"
    },
    {
        "name": "Mission Complete",
        "emoji": "🏆",
        "description": "Reached your 80 kg goal.",
        "condition": "weight <= 80"
    }
]


EXERCISE_LIBRARY = {
    "Barbell Bench Press": {
        "category": "Push",
        "equipment": "Barbell, bench, plates",
        "how": "Lie on the bench, grip the bar slightly wider than shoulder width, lower to mid-chest, then press up under control.",
        "tip": "Keep your feet planted and shoulder blades squeezed together."
    },
    "Barbell Squat": {
        "category": "Legs",
        "equipment": "Barbell, plates",
        "how": "Stand with feet shoulder-width apart, brace your core, squat down under control, then drive back up through your heels.",
        "tip": "Keep your chest up and knees tracking over your toes."
    },
    "Romanian Deadlift": {
        "category": "Legs",
        "equipment": "Barbell or dumbbells",
        "how": "Hold the weight in front of your thighs, push your hips back, keep your knees slightly bent and lower until you feel your hamstrings stretch.",
        "tip": "This is a hip hinge, not a squat."
    },
    "Walking Lunges": {
        "category": "Legs",
        "equipment": "Dumbbells optional",
        "how": "Step forward, lower both knees, then drive through the front heel to step into the next lunge.",
        "tip": "Keep your torso upright and controlled."
    },
    "Barbell Deadlift": {
        "category": "Full Body",
        "equipment": "Barbell, plates",
        "how": "Stand with the bar over mid-foot, hinge down, grip the bar, brace your core, and drive through the floor to stand tall.",
        "tip": "Keep the bar close to your body throughout."
    },
    "Barbell Bent-over Row": {
        "category": "Pull",
        "equipment": "Barbell, plates",
        "how": "Hinge forward with a flat back and pull the bar towards your lower ribs.",
        "tip": "Avoid jerking the weight. Pull with control."
    },
    "Dumbbell Shoulder Press": {
        "category": "Push",
        "equipment": "Dumbbells",
        "how": "Start with dumbbells at shoulder height, brace your core, and press overhead.",
        "tip": "Avoid arching your lower back."
    },
    "Band Face Pull": {
        "category": "Pull",
        "equipment": "Resistance bands",
        "how": "Anchor the band at face height, pull towards your face with elbows high, then return slowly.",
        "tip": "Excellent for posture and shoulder health."
    },
    "FitXR Combat": {
        "category": "Cardio",
        "equipment": "Meta/Oculus headset",
        "how": "Choose a boxing or combat class and keep moving throughout the session.",
        "tip": "Focus on consistent movement rather than perfect punches."
    },
    "Treadmill Incline Walk": {
        "category": "Cardio",
        "equipment": "Treadmill",
        "how": "Walk at a brisk pace with a light-to-moderate incline.",
        "tip": "You should be breathing harder but still able to speak."
    }
}
def load_log():
    columns = [
        "date", "weight", "workout_done", "workout_type",
        "fitxr_minutes", "fitxr_calories", "steps",
        "water_litres", "protein_grams", "energy",
        "meal_score", "notes"
    ]

    if not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=columns)

    try:
        return pd.read_csv(LOG_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=columns)


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
    return int(df["workout_done"].sum())


def current_streak(df):
    if df.empty:
        return 0

    done = df[df["workout_done"] == True]["date"].dropna().unique().tolist()
    done = set(done)

    streak = 0
    current = date.today()

    while current.isoformat() in done:
        streak += 1
        current = current - pd.Timedelta(days=1)

    return streak


def meal_colour(score):
    if score >= 9:
        return "🟢 Green"
    if score >= 7:
        return "🟡 Amber"
    return "🔴 Red"


df = load_log()
today = datetime.now().strftime("%A")
today_workout = WORKOUTS[today]

weight_now = latest_weight(df)
lost = START_WEIGHT - weight_now
remaining = weight_now - TARGET_WEIGHT
progress = max(0, min(100, (lost / (START_WEIGHT - TARGET_WEIGHT)) * 100))
completed = workout_count(df)
streak = current_streak(df)

st.markdown("""
<style>
body {
    background: #f4f6fb;
}
.block-container {
    padding-top: 1rem;
}
.hero {
    background: linear-gradient(135deg, #111827, #1e3a8a, #7c3aed);
    padding: 32px;
    border-radius: 30px;
    color: white;
    margin-bottom: 25px;
}
.hero h1 {
    font-size: 44px;
    margin-bottom: 0;
}
.hero p {
    color: #dbeafe;
    font-size: 18px;
}
.card {
    background: white;
    padding: 22px;
    border-radius: 24px;
    box-shadow: 0 10px 30px rgba(15,23,42,0.08);
    border: 1px solid #e5e7eb;
}
.metric-label {
    color: #64748b;
    font-size: 14px;
}
.metric-value {
    color: #0f172a;
    font-size: 32px;
    font-weight: 800;
}
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
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>80kg Mission Coach 💪</h1>
    <p>Personalised coaching dashboard for Femi: garage gym, FitXR, Nigerian food, fat loss and consistency.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Current Weight</div>
        <div class="metric-value">{weight_now:.1f} kg</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Weight Lost</div>
        <div class="metric-value">{lost:.1f} kg</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">July Workouts</div>
        <div class="metric-value">{completed}/{JULY_WORKOUT_TARGET}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Current Streak</div>
        <div class="metric-value">{streak} days</div>
    </div>
    """, unsafe_allow_html=True)

st.progress(progress / 100)
st.caption(f"Mission progress: {progress:.1f}% complete — {remaining:.1f} kg left to reach 80 kg.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard",
    "💪 Today’s Workout",
    "📝 Log Progress",
    "📊 Charts",
    "🍛 Meal Coach"
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
        st.markdown("""
        <div class="card">
            <h3>Coach Focus</h3>
            <p>Do not chase perfection. Complete the session, log it, drink water, and keep the streak alive.</p>
            <p><b>Today’s minimum:</b> 20 minutes still counts.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="margin-top:15px;">
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

    st.info("Coach note: use lighter weights if needed. Good form first, progress second.")

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
                "notes": notes
            })
            st.success("Saved. Another step towards 80 kg.")
            st.rerun()

with tab4:
    st.header("Progress Charts")

    if df.empty:
        st.warning("No logs yet. Add your first entry.")
    else:
        chart_df = df.copy()
        chart_df["date"] = pd.to_datetime(chart_df["date"])

        fig_weight = px.line(chart_df, x="date", y="weight", markers=True, title="Weight Progress")
        fig_weight.add_hline(y=TARGET_WEIGHT, line_dash="dash", annotation_text="80 kg target")
        st.plotly_chart(fig_weight, use_container_width=True)

        col_a, col_b = st.columns(2)

        with col_a:
            fig_steps = px.bar(chart_df, x="date", y="steps", title="Steps")
            st.plotly_chart(fig_steps, use_container_width=True)

        with col_b:
            fig_fitxr = px.bar(chart_df, x="date", y="fitxr_calories", title="FitXR Calories")
            st.plotly_chart(fig_fitxr, use_container_width=True)

        st.dataframe(chart_df.sort_values("date", ascending=False), use_container_width=True)

with tab5:
    st.header("Meal Coach")

    st.markdown("""
    Use this section to rate your meals using a simple traffic light system.

    **Green:** great meal for fat loss  
    **Amber:** decent, one small improvement  
    **Red:** enjoy occasionally, not daily
    """)

    score = st.slider("Meal score", 1, 10, 8)
    st.metric("Meal Category", meal_colour(score))

    meal = st.text_area("Describe the meal")

    if st.button("Get Basic Coach Feedback"):
        if score >= 9:
            st.success("Great meal. Keep it in your regular rotation.")
        elif score >= 7:
            st.warning("Good meal. Look for one small improvement: portion, oil, sugar or protein.")
        else:
            st.error("This is more of a treat meal. Enjoy it, but return to your normal plan next meal.")

        st.write("For Nigerian meals, focus on:")
        st.write("- Protein first: chicken, fish, turkey, eggs, beans or beef.")
        st.write("- Rice portion: about one fist-sized serving.")
        st.write("- Stew: flavour is fine, but avoid excess oil.")
        st.write("- Water: aim for 2.5–3 litres daily.")
with tab6:
    st.header("Achievement Badges")

    workouts = workout_count(df)
    weight = latest_weight(df)

    cols = st.columns(3)

    for i, badge in enumerate(ACHIEVEMENTS):
        unlocked = False

        if badge["condition"] == "workouts >= 1":
            unlocked = workouts >= 1
        elif badge["condition"] == "workouts >= 5":
            unlocked = workouts >= 5
        elif badge["condition"] == "workouts >= 10":
            unlocked = workouts >= 10
        elif badge["condition"] == "weight <= 92":
            unlocked = weight <= 92
        elif badge["condition"] == "weight <= 90":
            unlocked = weight <= 90
        elif badge["condition"] == "weight <= 85":
            unlocked = weight <= 85
        elif badge["condition"] == "weight <= 80":
            unlocked = weight <= 80

        with cols[i % 3]:
            if unlocked:
                st.success(f"{badge['emoji']} **{badge['name']}**\n\n{badge['description']}")
            else:
                st.info(f"🔒 **{badge['name']}**\n\n{badge['description']}")


with tab7:
    st.header("Garage Gym Exercise Library")

    selected_category = st.selectbox(
        "Filter by category",
        ["All", "Push", "Pull", "Legs", "Full Body", "Cardio"]
    )

    for name, details in EXERCISE_LIBRARY.items():
        if selected_category != "All" and details["category"] != selected_category:
            continue

        with st.expander(name):
            st.write(f"**Category:** {details['category']}")
            st.write(f"**Equipment:** {details['equipment']}")
            st.write(f"**How to do it:** {details['how']}")
            st.write(f"**Coach tip:** {details['tip']}")
