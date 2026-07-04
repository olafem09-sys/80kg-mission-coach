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
    "date",
    "weight",
    "workout_done",
    "workout_type",
    "planned_exercises_done",
    "extra_exercises_done",
    "manual_exercises_done",
    "fitxr_minutes",
    "fitxr_calories",
    "steps",
    "water_litres",
    "protein_grams",
    "energy",
    "meal_score",
    "daily_score",
    "notes"
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
        "video": "assets/videos/bench_press.mp4",
        "how": "Lie flat on the bench with your eyes under the bar. Grip slightly wider than shoulder width. Keep your feet planted, squeeze your shoulder blades together, lower the bar to mid-chest, then press up under control.",
        "mistakes": "Avoid bouncing the bar off your chest, lifting your hips, or flaring your elbows too wide.",
        "tip": "Use a weight that allows all reps with control. Stop 1–2 reps before failure while rebuilding the habit."
    },
    "Incline Dumbbell Press": {
        "category": "Push",
        "equipment": "Adjustable bench and dumbbells",
        "muscles": "Upper chest, shoulders and triceps",
        "video": "assets/videos/incline_dumbbell_press.mp4",
        "how": "Set the bench to an incline. Start with dumbbells at chest level, press upward, then lower slowly.",
        "mistakes": "Avoid setting the bench too steep or letting the dumbbells drift too wide.",
        "tip": "Keep the movement controlled and focus on feeling the chest working."
    },
    "Standing Shoulder Press": {
        "category": "Push",
        "equipment": "Barbell or dumbbells",
        "muscles": "Shoulders, triceps and core",
        "video": "assets/videos/shoulder_press.mp4",
        "how": "Start with the bar or dumbbells at shoulder height. Brace your core, press overhead, then lower under control.",
        "mistakes": "Avoid arching your lower back or using leg drive unless intentionally doing a push press.",
        "tip": "Squeeze your glutes and brace your stomach before pressing."
    },
    "Dumbbell Shoulder Press": {
        "category": "Push",
        "equipment": "Dumbbells",
        "muscles": "Shoulders and triceps",
        "video": "assets/videos/dumbbell_shoulder_press.mp4",
        "how": "Start with dumbbells at shoulder height. Brace your core and press overhead until your arms are almost straight, then lower slowly.",
        "mistakes": "Avoid arching your lower back or rushing the reps.",
        "tip": "Seated is easier to control; standing challenges your core more."
    },
    "Band Triceps Pushdown": {
        "category": "Push",
        "equipment": "Resistance bands",
        "muscles": "Triceps",
        "video": "assets/videos/band_triceps_pushdown.mp4",
        "how": "Anchor the band above head height. Keep elbows tucked, push the band down until arms are straight, then return slowly.",
        "mistakes": "Avoid letting your elbows flare or using your shoulders to swing.",
        "tip": "Pause briefly at the bottom to squeeze the triceps."
    },

    "Barbell Squat": {
        "category": "Legs",
        "equipment": "Barbell, plates",
        "muscles": "Quads, glutes, hamstrings and core",
        "video": "assets/videos/barbell_squat.mp4",
        "how": "Stand with feet around shoulder-width apart. Brace your core, keep your chest up, sit the hips back and down, then drive through your heels to stand tall.",
        "mistakes": "Avoid knees collapsing inward, heels lifting, or rounding your back.",
        "tip": "Start lighter and focus on depth, control and balance."
    },
    "Goblet Squat": {
        "category": "Legs",
        "equipment": "Dumbbell or kettlebell",
        "muscles": "Quads, glutes and core",
        "video": "assets/videos/goblet_squat.mp4",
        "how": "Hold one dumbbell close to your chest. Squat down under control, keep your elbows inside your knees, then stand tall.",
        "mistakes": "Avoid leaning forward excessively or letting your heels lift.",
        "tip": "Great for learning squat form safely."
    },
    "Romanian Deadlift": {
        "category": "Legs",
        "equipment": "Barbell or dumbbells",
        "muscles": "Hamstrings, glutes and lower back",
        "video": "assets/videos/romanian_deadlift.mp4",
        "how": "Hold the bar or dumbbells in front of your thighs. Keep knees slightly bent, push your hips backwards, lower the weight close to your legs, then squeeze your glutes to return upright.",
        "mistakes": "Do not turn it into a squat. The movement should come mainly from the hips.",
        "tip": "You should feel a strong stretch in your hamstrings, not pain in your lower back."
    },
    "Walking Lunges": {
        "category": "Legs",
        "equipment": "Bodyweight or dumbbells",
        "muscles": "Quads, glutes, hamstrings and balance muscles",
        "video": "assets/videos/walking_lunges.mp4",
        "how": "Step forward, lower until both knees are bent, then drive through the front heel to move into the next rep.",
        "mistakes": "Avoid leaning too far forward or taking very short steps.",
        "tip": "Keep your torso upright and take your time."
    },
    "Calf Raises": {
        "category": "Legs",
        "equipment": "Bodyweight, dumbbells or barbell",
        "muscles": "Calves",
        "video": "assets/videos/calf_raises.mp4",
        "how": "Stand tall, rise onto your toes, pause at the top, then lower slowly.",
        "mistakes": "Avoid bouncing quickly through the movement.",
        "tip": "Use a slow tempo and full range of motion."
    },
    "Band Glute Kickback": {
        "category": "Legs",
        "equipment": "Resistance bands",
        "muscles": "Glutes and hamstrings",
        "video": "assets/videos/band_glute_kickback.mp4",
        "how": "Anchor the band low, attach around the foot or ankle, then kick backwards while keeping your torso stable.",
        "mistakes": "Avoid twisting your hips or arching your lower back.",
        "tip": "Squeeze the glute at the top of the movement."
    },

    "Barbell Deadlift": {
        "category": "Full Body",
        "equipment": "Barbell, plates",
        "muscles": "Glutes, hamstrings, back, traps, grip and core",
        "video": "assets/videos/deadlift.mp4",
        "how": "Stand with the bar over mid-foot. Hinge down, grip the bar, brace your core, keep the bar close, and push the floor away as you stand tall.",
        "mistakes": "Avoid rounding your back or letting the bar drift away from your body.",
        "tip": "Technique matters more than heavy weight, especially while returning to training."
    },
    "Kettlebell Swings": {
        "category": "Full Body",
        "equipment": "Kettlebell",
        "muscles": "Glutes, hamstrings, core, back and conditioning",
        "video": "assets/videos/kettlebell_swings.mp4",
        "how": "Hinge at the hips, swing the kettlebell back, then drive hips forward to swing it to chest height.",
        "mistakes": "Avoid squatting the movement or lifting with your arms.",
        "tip": "The power comes from your hips, not your shoulders."
    },
    "Press-ups": {
        "category": "Push",
        "equipment": "Bodyweight",
        "muscles": "Chest, shoulders, triceps and core",
        "video": "assets/videos/press_ups.mp4",
        "how": "Hands under shoulders, body straight, lower chest towards the floor, then press back up.",
        "mistakes": "Avoid hips sagging or flaring elbows too wide.",
        "tip": "Use incline press-ups on the bench if standard press-ups are too hard."
    },

    "Barbell Bent-over Row": {
        "category": "Pull",
        "equipment": "Barbell, plates",
        "muscles": "Upper back, lats, rear shoulders and biceps",
        "video": "assets/videos/bent_over_row.mp4",
        "how": "Hinge forward with a flat back. Pull the bar towards your lower ribs, squeeze your shoulder blades, then lower under control.",
        "mistakes": "Avoid jerking the weight or standing too upright.",
        "tip": "Keep your core tight and pull with your back, not just your arms."
    },
    "One-arm Dumbbell Row": {
        "category": "Pull",
        "equipment": "Dumbbell and bench",
        "muscles": "Lats, upper back and biceps",
        "video": "assets/videos/one_arm_dumbbell_row.mp4",
        "how": "Support one hand on the bench, keep your back flat, pull the dumbbell towards your hip, then lower slowly.",
        "mistakes": "Avoid twisting your body or shrugging the shoulder.",
        "tip": "Think about pulling with your elbow, not your hand."
    },
    "Pull-ups": {
        "category": "Pull",
        "equipment": "Pull-up bar",
        "muscles": "Lats, upper back, biceps and grip",
        "video": "assets/videos/pull_ups.mp4",
        "how": "Grip the bar, pull your chest towards it, then lower under control.",
        "mistakes": "Avoid half reps or swinging excessively.",
        "tip": "Use controlled negatives if full pull-ups are difficult."
    },
    "Band Face Pull": {
        "category": "Pull",
        "equipment": "Resistance bands",
        "muscles": "Rear shoulders, upper back and rotator cuff",
        "video": "assets/videos/band_face_pull.mp4",
        "how": "Anchor the band at face height. Pull towards your face with elbows high, pause, then return slowly.",
        "mistakes": "Avoid shrugging your shoulders or using momentum.",
        "tip": "Excellent for posture and shoulder health. Keep this in the plan."
    },
    "Band Biceps Curl": {
        "category": "Pull",
        "equipment": "Resistance bands",
        "muscles": "Biceps",
        "video": "assets/videos/band_biceps_curl.mp4",
        "how": "Stand on the band, hold handles, curl towards your shoulders, then lower slowly.",
        "mistakes": "Avoid swinging your upper body.",
        "tip": "Keep elbows close to your sides."
    },

    "Plank": {
        "category": "Core",
        "equipment": "Bodyweight",
        "muscles": "Core, shoulders and glutes",
        "video": "assets/videos/plank.mp4",
        "how": "Elbows under shoulders, body in a straight line, squeeze glutes and brace your abs. Breathe steadily.",
        "mistakes": "Avoid hips sagging or sticking too high.",
        "tip": "Quality matters more than duration."
    },
    "Dead Bug": {
        "category": "Core",
        "equipment": "Bodyweight",
        "muscles": "Core and hip control",
        "video": "assets/videos/dead_bug.mp4",
        "how": "Lie on your back, arms up, knees bent. Lower opposite arm and leg slowly, then return.",
        "mistakes": "Avoid arching your lower back.",
        "tip": "Move slowly and keep your lower back gently pressed down."
    },
    "Hanging Knee Raises": {
        "category": "Core",
        "equipment": "Pull-up bar",
        "muscles": "Abs, hip flexors and grip",
        "video": "assets/videos/hanging_knee_raises.mp4",
        "how": "Hang from the bar and raise your knees towards your chest under control.",
        "mistakes": "Avoid swinging the body excessively.",
        "tip": "Start with bent knees and controlled reps."
    },

    "FitXR Combat": {
        "category": "Cardio",
        "equipment": "Oculus / Meta headset",
        "muscles": "Cardio system, shoulders, arms, core and legs",
        "video": "",
        "how": "Choose a boxing or combat class. Keep your guard up, move your feet, punch with control and keep breathing.",
        "mistakes": "Avoid over-swinging your arms or stopping completely between combinations.",
        "tip": "Brilliant for fat loss because it feels more like a game than cardio."
    },
    "Treadmill Incline Walk": {
        "category": "Cardio",
        "equipment": "Treadmill",
        "muscles": "Cardio system, calves, glutes and legs",
        "video": "",
        "how": "Walk briskly with a moderate incline. Keep posture tall and avoid holding the rails unless needed.",
        "mistakes": "Avoid setting the incline so high that your form collapses.",
        "tip": "Excellent low-impact fat-loss tool."
    },
    "Treadmill Brisk Walk": {
        "category": "Cardio",
        "equipment": "Treadmill",
        "muscles": "Cardio system and legs",
        "video": "",
        "how": "Walk at a pace that raises your breathing but still allows you to speak in short sentences.",
        "mistakes": "Avoid holding the rails unless needed for balance.",
        "tip": "Useful on recovery days or when motivation is low."
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
