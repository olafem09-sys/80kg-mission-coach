# Mission 80 Coach Database

## SQLite

The application currently uses SQLite.

Later versions may migrate to PostgreSQL while preserving the data model.

---

## Core Tables

- user_profile
- workout_log
- exercise_log
- food_database
- nutrition_log
- weight_log
- measurements
- coach_history

---

## Relationships

```
user_profile
    │
    ├── workout_log
    │       │
    │       └── exercise_log
    │
    ├── nutrition_log
    │
    ├── weight_log
    │
    └── measurements
```

---

## Future

Future releases will add:

- AI coaching history
- Sleep tracking
- Heart-rate data
- Garmin integration
- Google Fit integration