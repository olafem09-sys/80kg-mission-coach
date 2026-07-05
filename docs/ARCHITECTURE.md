# Mission 80 Coach Architecture

## Overview

Mission 80 Coach is a modular fitness and lifestyle coaching platform designed to support long-term weight loss, strength development and healthy habits.

The application is built using Streamlit with a modular architecture to support future migration to an Android application.

---

## Project Structure

```
app.py
components/
pages/
utils/
data/
assets/
docs/
```

---

## Responsibilities

### app.py

Application entry point.

Responsible for:

- Initialising Streamlit
- Loading configuration
- Loading theme
- Initialising database
- Routing between pages

---

### components/

Reusable UI components.

Examples:

- Cards
- Navigation
- Styling

---

### pages/

Each page contains one render() function.

Pages:

- Dashboard
- Workout
- Exercise Library
- Nutrition
- Progress
- AI Coach
- Settings

---

### utils/

Business logic.

Examples:

- Workout engine
- Database
- Scoring
- Food recommendations

---

### data/

SQLite database

Reference data

Backups

---

### assets/

Images

Videos

Icons

Logos

---

## Principles

- Modular
- Mobile-first
- Reusable
- Testable
- Android-ready