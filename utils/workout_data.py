"""
Mission 80 Coach
Workout and Exercise Data
Version 2.0
"""

WEEKLY_WORKOUT_PLAN = {
    "Monday": {
        "title": "Upper Body + Core",
        "focus": "Chest, shoulders, triceps and core",
        "duration": "45–60 mins",
        "exercises": [
            "Barbell Bench Press",
            "Standing Shoulder Press",
            "Incline Dumbbell Press",
            "Band Triceps Pushdown",
            "Plank",
            "Treadmill Brisk Walk",
        ],
    },
    "Tuesday": {
        "title": "FitXR Cardio",
        "focus": "Fat burn and conditioning",
        "duration": "30–45 mins",
        "exercises": [
            "FitXR Combat",
            "Kettlebell Swings",
            "Stretching",
        ],
    },
    "Wednesday": {
        "title": "Lower Body",
        "focus": "Legs, glutes and core",
        "duration": "45–60 mins",
        "exercises": [
            "Barbell Squat",
            "Romanian Deadlift",
            "Walking Lunges",
            "Band Glute Kickback",
            "Calf Raises",
            "Plank",
        ],
    },
    "Thursday": {
        "title": "Recovery Walk + Mobility",
        "focus": "Recovery and movement",
        "duration": "30–45 mins",
        "exercises": [
            "Treadmill Incline Walk",
            "Hip Flexor Stretch",
            "Hamstring Stretch",
            "Child’s Pose",
            "Shoulder Circles",
        ],
    },
    "Friday": {
        "title": "Full Body Strength",
        "focus": "Strength and muscle retention",
        "duration": "45–60 mins",
        "exercises": [
            "Barbell Deadlift",
            "Barbell Bench Press",
            "Barbell Bent-over Row",
            "Dumbbell Shoulder Press",
            "Goblet Squat",
            "Band Face Pull",
        ],
    },
    "Saturday": {
        "title": "FitXR Cardio",
        "focus": "Fun cardio and calorie burn",
        "duration": "45–60 mins",
        "exercises": [
            "FitXR Combat",
            "Treadmill Incline Walk",
            "Stretching",
        ],
    },
    "Sunday": {
        "title": "Rest Day",
        "focus": "Recovery and weekly review",
        "duration": "Optional",
        "exercises": [
    "Rest day",
    "Optional 20–30 minute easy walk",
    "Weekly check-in",
],
    },
}


EXERCISE_LIBRARY = {
    "Barbell Bench Press": {
        "category": "Push",
        "equipment": ["Barbell", "Bench", "Weight Plates"],
        "muscles": ["Chest", "Shoulders", "Triceps"],
        "difficulty": "Intermediate",
        "video": "assets/videos/bench_press.mp4",
        "instructions": "Lie on the bench with your eyes under the bar. Grip slightly wider than shoulder width. Lower the bar to mid-chest, then press up under control.",
        "common_mistakes": "Bouncing the bar, lifting the hips, flaring elbows too wide.",
        "coach_tip": "Keep your feet planted and squeeze your shoulder blades together.",
        "alternatives": ["Dumbbell Bench Press", "Press-ups", "Incline Dumbbell Press"],
    },
    "Incline Dumbbell Press": {
        "category": "Push",
        "equipment": ["Dumbbells", "Bench"],
        "muscles": ["Upper Chest", "Shoulders", "Triceps"],
        "difficulty": "Beginner",
        "video": "assets/videos/incline_dumbbell_press.mp4",
        "instructions": "Set the bench to a moderate incline. Press the dumbbells from chest level upwards, then lower slowly.",
        "common_mistakes": "Bench too steep, rushing reps, letting dumbbells drift too wide.",
        "coach_tip": "Use controlled reps and keep the chest engaged.",
        "alternatives": ["Barbell Bench Press", "Press-ups"],
    },
    "Standing Shoulder Press": {
        "category": "Push",
        "equipment": ["Barbell", "Dumbbells"],
        "muscles": ["Shoulders", "Triceps", "Core"],
        "difficulty": "Intermediate",
        "video": "assets/videos/shoulder_press.mp4",
        "instructions": "Start with the bar or dumbbells at shoulder height. Brace your core and press overhead.",
        "common_mistakes": "Overarching the lower back or using excessive leg drive.",
        "coach_tip": "Squeeze your glutes and brace your stomach before pressing.",
        "alternatives": ["Dumbbell Shoulder Press", "Pike Press-up"],
    },
    "Dumbbell Shoulder Press": {
        "category": "Push",
        "equipment": ["Dumbbells"],
        "muscles": ["Shoulders", "Triceps"],
        "difficulty": "Beginner",
        "video": "assets/videos/dumbbell_shoulder_press.mp4",
        "instructions": "Start with dumbbells at shoulder height. Press overhead, then lower slowly.",
        "common_mistakes": "Arching the back, rushing reps, using too much weight.",
        "coach_tip": "Seated is easier to control; standing challenges your core more.",
        "alternatives": ["Standing Shoulder Press", "Lateral Raise"],
    },
    "Band Triceps Pushdown": {
        "category": "Push",
        "equipment": ["Resistance Bands"],
        "muscles": ["Triceps"],
        "difficulty": "Beginner",
        "video": "assets/videos/band_triceps_pushdown.mp4",
        "instructions": "Anchor the band high. Keep elbows tucked and push down until arms are straight.",
        "common_mistakes": "Elbows flaring or swinging the shoulders.",
        "coach_tip": "Pause at the bottom and squeeze the triceps.",
        "alternatives": ["Bench Dips", "Overhead Triceps Extension"],
    },
    "Press-ups": {
        "category": "Push",
        "equipment": ["Bodyweight"],
        "muscles": ["Chest", "Shoulders", "Triceps", "Core"],
        "difficulty": "Beginner",
        "video": "assets/videos/press_ups.mp4",
        "instructions": "Hands under shoulders, body straight, lower chest towards the floor, press back up.",
        "common_mistakes": "Hips sagging, elbows flaring, shallow reps.",
        "coach_tip": "Use incline press-ups on the bench if needed.",
        "alternatives": ["Barbell Bench Press", "Dumbbell Bench Press"],
    },
    "Barbell Squat": {
        "category": "Legs",
        "equipment": ["Barbell", "Weight Plates"],
        "muscles": ["Quads", "Glutes", "Hamstrings", "Core"],
        "difficulty": "Intermediate",
        "video": "assets/videos/barbell_squat.mp4",
        "instructions": "Brace your core, keep chest up, squat down under control, then drive back up.",
        "common_mistakes": "Knees collapsing, heels lifting, rounding the back.",
        "coach_tip": "Start lighter and focus on depth and control.",
        "alternatives": ["Goblet Squat", "Split Squat"],
    },
    "Goblet Squat": {
        "category": "Legs",
        "equipment": ["Dumbbell", "Kettlebell"],
        "muscles": ["Quads", "Glutes", "Core"],
        "difficulty": "Beginner",
        "video": "assets/videos/goblet_squat.mp4",
        "instructions": "Hold a dumbbell close to your chest. Squat down under control and stand tall.",
        "common_mistakes": "Leaning too far forward or lifting heels.",
        "coach_tip": "Excellent for learning squat form safely.",
        "alternatives": ["Barbell Squat", "Bodyweight Squat"],
    },
    "Romanian Deadlift": {
        "category": "Legs",
        "equipment": ["Barbell", "Dumbbells"],
        "muscles": ["Hamstrings", "Glutes", "Lower Back"],
        "difficulty": "Intermediate",
        "video": "assets/videos/romanian_deadlift.mp4",
        "instructions": "Push hips back, keep knees slightly bent, lower weight close to legs, then squeeze glutes to stand.",
        "common_mistakes": "Turning it into a squat or rounding the back.",
        "coach_tip": "Feel the stretch in your hamstrings, not pain in your lower back.",
        "alternatives": ["Dumbbell Romanian Deadlift", "Hip Thrust"],
    },
    "Walking Lunges": {
        "category": "Legs",
        "equipment": ["Bodyweight", "Dumbbells"],
        "muscles": ["Quads", "Glutes", "Hamstrings"],
        "difficulty": "Beginner",
        "video": "assets/videos/walking_lunges.mp4",
        "instructions": "Step forward, lower both knees, drive through the front heel and continue forward.",
        "common_mistakes": "Short steps, leaning too far forward, rushing.",
        "coach_tip": "Keep your torso upright and move with control.",
        "alternatives": ["Reverse Lunges", "Split Squat"],
    },
    "Calf Raises": {
        "category": "Legs",
        "equipment": ["Bodyweight", "Dumbbells", "Barbell"],
        "muscles": ["Calves"],
        "difficulty": "Beginner",
        "video": "assets/videos/calf_raises.mp4",
        "instructions": "Rise onto your toes, pause at the top, lower slowly.",
        "common_mistakes": "Bouncing quickly or using half range.",
        "coach_tip": "Use slow reps and full range.",
        "alternatives": ["Single-leg Calf Raise"],
    },
    "Band Glute Kickback": {
        "category": "Legs",
        "equipment": ["Resistance Bands"],
        "muscles": ["Glutes", "Hamstrings"],
        "difficulty": "Beginner",
        "video": "assets/videos/band_glute_kickback.mp4",
        "instructions": "Anchor the band low and kick backwards while keeping your torso stable.",
        "common_mistakes": "Twisting hips or arching lower back.",
        "coach_tip": "Squeeze the glute at the top.",
        "alternatives": ["Glute Bridge", "Hip Thrust"],
    },
    "Barbell Deadlift": {
        "category": "Full Body",
        "equipment": ["Barbell", "Weight Plates"],
        "muscles": ["Glutes", "Hamstrings", "Back", "Traps", "Grip", "Core"],
        "difficulty": "Intermediate",
        "video": "assets/videos/deadlift.mp4",
        "instructions": "Bar over mid-foot, brace, keep bar close, push the floor away and stand tall.",
        "common_mistakes": "Rounding back, bar drifting away, jerking the lift.",
        "coach_tip": "Technique first. Do not chase heavy weight too early.",
        "alternatives": ["Romanian Deadlift", "Kettlebell Deadlift"],
    },
    "Kettlebell Swings": {
        "category": "Full Body",
        "equipment": ["Kettlebell"],
        "muscles": ["Glutes", "Hamstrings", "Core", "Back"],
        "difficulty": "Intermediate",
        "video": "assets/videos/kettlebell_swings.mp4",
        "instructions": "Hinge at the hips, swing the kettlebell back, then drive hips forward to chest height.",
        "common_mistakes": "Squatting the movement or lifting with arms.",
        "coach_tip": "The power comes from the hips.",
        "alternatives": ["Hip Hinge", "Romanian Deadlift"],
    },
    "Barbell Bent-over Row": {
        "category": "Pull",
        "equipment": ["Barbell", "Weight Plates"],
        "muscles": ["Upper Back", "Lats", "Rear Shoulders", "Biceps"],
        "difficulty": "Intermediate",
        "video": "assets/videos/bent_over_row.mp4",
        "instructions": "Hinge forward, keep back flat, pull bar towards lower ribs, lower under control.",
        "common_mistakes": "Jerking weight or standing too upright.",
        "coach_tip": "Pull with your back, not just your arms.",
        "alternatives": ["One-arm Dumbbell Row", "Band Row"],
    },
    "One-arm Dumbbell Row": {
        "category": "Pull",
        "equipment": ["Dumbbell", "Bench"],
        "muscles": ["Lats", "Upper Back", "Biceps"],
        "difficulty": "Beginner",
        "video": "assets/videos/one_arm_dumbbell_row.mp4",
        "instructions": "Support one hand on bench. Pull dumbbell towards your hip, then lower slowly.",
        "common_mistakes": "Twisting body or shrugging.",
        "coach_tip": "Think about pulling with your elbow.",
        "alternatives": ["Barbell Bent-over Row", "Band Row"],
    },
    "Pull-ups": {
        "category": "Pull",
        "equipment": ["Pull-up Bar"],
        "muscles": ["Lats", "Upper Back", "Biceps", "Grip"],
        "difficulty": "Advanced",
        "video": "assets/videos/pull_ups.mp4",
        "instructions": "Grip the bar, pull chest towards it, then lower under control.",
        "common_mistakes": "Swinging or using half reps.",
        "coach_tip": "Use slow negatives if full pull-ups are difficult.",
        "alternatives": ["Band-assisted Pull-up", "Band Lat Pulldown"],
    },
    "Band Face Pull": {
        "category": "Pull",
        "equipment": ["Resistance Bands"],
        "muscles": ["Rear Shoulders", "Upper Back", "Rotator Cuff"],
        "difficulty": "Beginner",
        "video": "assets/videos/band_face_pull.mp4",
        "instructions": "Anchor band at face height. Pull towards face with elbows high, pause, return slowly.",
        "common_mistakes": "Shrugging shoulders or using momentum.",
        "coach_tip": "Excellent for posture and shoulder health.",
        "alternatives": ["Band Pull-apart", "Rear Delt Fly"],
    },
    "Band Biceps Curl": {
        "category": "Pull",
        "equipment": ["Resistance Bands"],
        "muscles": ["Biceps"],
        "difficulty": "Beginner",
        "video": "assets/videos/band_biceps_curl.mp4",
        "instructions": "Stand on band, curl handles towards shoulders, lower slowly.",
        "common_mistakes": "Swinging upper body.",
        "coach_tip": "Keep elbows close to your sides.",
        "alternatives": ["Dumbbell Curl", "Barbell Curl"],
    },
    "Plank": {
        "category": "Core",
        "equipment": ["Bodyweight"],
        "muscles": ["Core", "Shoulders", "Glutes"],
        "difficulty": "Beginner",
        "video": "assets/videos/plank.mp4",
        "instructions": "Elbows under shoulders, body straight, squeeze glutes and brace abs.",
        "common_mistakes": "Hips sagging or too high.",
        "coach_tip": "Quality matters more than duration.",
        "alternatives": ["Dead Bug", "Side Plank"],
    },
    "Dead Bug": {
        "category": "Core",
        "equipment": ["Bodyweight"],
        "muscles": ["Core", "Hip Control"],
        "difficulty": "Beginner",
        "video": "assets/videos/dead_bug.mp4",
        "instructions": "Lie on back. Lower opposite arm and leg slowly while keeping lower back controlled.",
        "common_mistakes": "Arching the lower back.",
        "coach_tip": "Move slowly and keep tension.",
        "alternatives": ["Plank", "Bird Dog"],
    },
    "Hanging Knee Raises": {
        "category": "Core",
        "equipment": ["Pull-up Bar"],
        "muscles": ["Abs", "Hip Flexors", "Grip"],
        "difficulty": "Intermediate",
        "video": "assets/videos/hanging_knee_raises.mp4",
        "instructions": "Hang from bar and raise knees towards chest under control.",
        "common_mistakes": "Swinging excessively.",
        "coach_tip": "Start with bent knees and controlled reps.",
        "alternatives": ["Lying Knee Raises", "Dead Bug"],
    },
    "FitXR Combat": {
        "category": "Cardio",
        "equipment": ["Oculus", "Meta Headset"],
        "muscles": ["Cardio", "Shoulders", "Arms", "Core", "Legs"],
        "difficulty": "Beginner",
        "video": "",
        "instructions": "Choose a boxing or combat class. Keep your guard up, move your feet and punch with control.",
        "common_mistakes": "Over-swinging or stopping completely between combinations.",
        "coach_tip": "Excellent because it feels like a game, not cardio.",
        "alternatives": ["Treadmill Brisk Walk", "Treadmill Incline Walk"],
    },
    "Treadmill Incline Walk": {
        "category": "Cardio",
        "equipment": ["Treadmill"],
        "muscles": ["Cardio", "Calves", "Glutes", "Legs"],
        "difficulty": "Beginner",
        "video": "",
        "instructions": "Walk briskly with a moderate incline. Keep posture tall.",
        "common_mistakes": "Incline too high, holding rails too much.",
        "coach_tip": "Low-impact and excellent for fat loss.",
        "alternatives": ["Treadmill Brisk Walk", "Outdoor Walk"],
    },
    "Treadmill Brisk Walk": {
        "category": "Cardio",
        "equipment": ["Treadmill"],
        "muscles": ["Cardio", "Legs"],
        "difficulty": "Beginner",
        "video": "",
        "instructions": "Walk at a pace where breathing increases but you can still speak in short sentences.",
        "common_mistakes": "Too slow to challenge you or holding rails unnecessarily.",
        "coach_tip": "Useful on recovery days and low-motivation days.",
        "alternatives": ["Treadmill Incline Walk", "Outdoor Walk"],
    },
    "Stretching": {
        "category": "Mobility",
        "equipment": ["Bodyweight"],
        "muscles": ["Full Body"],
        "difficulty": "Beginner",
        "video": "",
        "instructions": "Use gentle stretches for hips, hamstrings, quads, shoulders and back.",
        "common_mistakes": "Forcing deep stretches or bouncing.",
        "coach_tip": "Stretching should reduce tension, not cause pain.",
        "alternatives": ["Mobility Flow", "Light Walk"],
    },
    "Hip Flexor Stretch": {
        "category": "Mobility",
        "equipment": ["Bodyweight"],
        "muscles": ["Hip Flexors", "Quads"],
        "difficulty": "Beginner",
        "video": "",
        "instructions": "Kneel with one leg forward. Gently shift hips forward until you feel a stretch.",
        "common_mistakes": "Overarching the lower back.",
        "coach_tip": "Squeeze the glute on the kneeling side.",
        "alternatives": ["Quad Stretch", "Mobility Flow"],
    },
    "Hamstring Stretch": {
        "category": "Mobility",
        "equipment": ["Bodyweight"],
        "muscles": ["Hamstrings"],
        "difficulty": "Beginner",
        "video": "",
        "instructions": "Extend one leg and hinge forward gently until you feel a stretch.",
        "common_mistakes": "Rounding aggressively or forcing range.",
        "coach_tip": "Keep the stretch gentle and controlled.",
        "alternatives": ["Standing Hamstring Stretch"],
    },
    "Child’s Pose": {
        "category": "Mobility",
        "equipment": ["Bodyweight"],
        "muscles": ["Back", "Hips", "Shoulders"],
        "difficulty": "Beginner",
        "video": "",
        "instructions": "Sit back towards your heels and reach arms forward on the floor.",
        "common_mistakes": "Holding breath or forcing the position.",
        "coach_tip": "Use it to calm breathing after training.",
        "alternatives": ["Cat-Cow Stretch"],
    },
    "Shoulder Circles": {
        "category": "Mobility",
        "equipment": ["Bodyweight"],
        "muscles": ["Shoulders"],
        "difficulty": "Beginner",
        "video": "",
        "instructions": "Move shoulders in controlled circles forwards and backwards.",
        "common_mistakes": "Rushing or shrugging too high.",
        "coach_tip": "Good warm-up before upper-body work.",
        "alternatives": ["Band Pull-apart", "Arm Circles"],
    },
    
}


def get_today_workout(day_name: str) -> dict:
    """Return workout plan for the supplied day name."""
    return WEEKLY_WORKOUT_PLAN.get(day_name, WEEKLY_WORKOUT_PLAN["Monday"])


def get_exercise_names() -> list[str]:
    """Return all exercise names sorted alphabetically."""
    return sorted(EXERCISE_LIBRARY.keys())


def get_exercises_by_category(category: str) -> dict:
    """Return exercises filtered by category."""
    if category == "All":
        return EXERCISE_LIBRARY

    return {
        name: details
        for name, details in EXERCISE_LIBRARY.items()
        if details["category"] == category
    }


def get_exercises_by_equipment(equipment: str) -> dict:
    """Return exercises filtered by equipment."""
    if equipment == "All":
        return EXERCISE_LIBRARY

    return {
        name: details
        for name, details in EXERCISE_LIBRARY.items()
        if equipment in details["equipment"]
    }


def search_exercises(search_term: str) -> dict:
    """Search exercise library by name, muscle, category or equipment."""
    if not search_term:
        return EXERCISE_LIBRARY

    term = search_term.lower()

    results = {}

    for name, details in EXERCISE_LIBRARY.items():
        searchable_text = " ".join(
            [
                name,
                details["category"],
                " ".join(details["equipment"]),
                " ".join(details["muscles"]),
                details["instructions"],
            ]
        ).lower()

        if term in searchable_text:
            results[name] = details

    return results