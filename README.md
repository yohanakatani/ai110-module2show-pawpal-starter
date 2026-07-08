# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Priority scheduling** — high-priority tasks are always planned first
- **Time-based sorting** — tasks display in chronological order by start time
- **Conflict warnings** — the app flags two tasks scheduled at the same time
- **Recurring tasks** — daily and weekly tasks auto-reschedule after completion
- **Task filtering** — filter by pet name or completion status
- **Multi-pet support** — one owner can manage tasks across multiple pets

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Today's Schedule - Jordan (60 min available)

Mochi (dog)
  Morning walk           30 min   high
  Give medication        10 min   high
  Brushing               20 min   low

Luna (cat)
  Feeding                10 min   medium

Skipped (not enough time):
  Brushing               20 min   low
```

## 🏆 Priority-Based Scheduling

Tasks are sorted by priority first (high → medium → low), then by scheduled
time as a tiebreaker. This ensures critical tasks like medication are always
surfaced before lower-priority ones, regardless of when they're scheduled.

**Method:** `Scheduler.sort_by_priority_then_time()`

```
=== Sorted by Time Only ===
  07:00  Brushing               [low]
  07:30  Feeding                [medium]
  08:00  Give medication        [high]
  09:00  Morning walk           [high]

=== Sorted by Priority, then Time ===
  08:00  Give medication        [high]
  09:00  Morning walk           [high]
  07:30  Feeding                [medium]
  07:00  Brushing               [low]
```

## 💾 Data Persistence

PawPal+ saves and loads all data to `data.json` using custom dictionary
serialization — no external libraries required.

**Workflow:**
1. After building a schedule, call `scheduler.save_to_json("data.json")` to persist the current state.
2. On the next run, call `Scheduler.load_from_json("data.json")` to restore all owners, pets, and tasks exactly as they were.

**Files modified:** `pawpal_system.py` (added `save_to_json` and `load_from_json` to `Scheduler`)

**JSON format:**
```json
{
  "owner": {
    "name": "Jordan",
    "available_minutes": 60,
    "pets": [
      {
        "name": "Mochi",
        "species": "dog",
        "tasks": [
          {
            "title": "Morning walk",
            "duration_minutes": 30,
            "priority": "high",
            "frequency": "daily",
            "completed": false,
            "time": "08:00",
            "due_date": "2026-07-08"
          }
        ]
      }
    ]
  }
}
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The test suite covers:
- **Sorting correctness** — tasks come back in chronological order by time
- **Recurrence logic** — completing a daily task auto-creates the next occurrence
- **Conflict detection** — scheduler flags two tasks at the same start time
- **Edge cases** — empty task list, no conflicts, and non-recurring tasks

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\yohan\Codepath\AI110\ai110-module2show-pawpal-starter
collected 7 items

tests/test_pawpal.py::test_high_priority_tasks_planned_first PASSED      [ 14%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 28%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_occurrence PASSED [ 42%]
tests/test_pawpal.py::test_generate_schedule_with_no_tasks PASSED        [ 57%]
tests/test_pawpal.py::test_get_conflicts_detects_same_time PASSED        [ 71%]
tests/test_pawpal.py::test_get_conflicts_no_conflicts PASSED             [ 85%]
tests/test_pawpal.py::test_once_task_does_not_recur PASSED               [100%]

============================== 7 passed in 0.06s ==============================
```

**Confidence Level: ★★★★☆** — Core scheduling logic is well covered. Duration-based conflict detection and multi-pet edge cases could use more tests.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all pending tasks by scheduled time in HH:MM format using a lambda key |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by pet name, completion status, or both |
| Conflict detection | `Scheduler.get_conflicts()` | Returns warning messages for tasks sharing the exact same start time |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_complete()` | When a daily/weekly task is completed, a new instance is auto-scheduled using `timedelta` |

## 📸 Demo Walkthrough

1. **Set up your profile** — Enter your name, your pet's name, species, and how many minutes you have today. Click "Set up owner & pet."
2. **Add tasks** — Enter a task title, duration, priority, start time, and frequency. Click "Add task." Tasks appear in the table sorted by time automatically.
3. **Watch for conflicts** — If two tasks share the same start time, a warning banner appears immediately below the table.
4. **Generate your schedule** — Click "Generate schedule." High-priority tasks are planned first. Tasks that don't fit in your time budget are listed under "Skipped."
5. **Recurring tasks** — Daily and weekly tasks auto-create their next occurrence when marked complete, so you never lose track.

**Sample CLI output from `python main.py`:**

```
=== Sorted by Time ===
  07:00  Give medication        10 min  [high]
  08:00  Morning walk           30 min  [high]
  09:00  Feeding                10 min  [medium]
  10:00  Brushing               20 min  [low]

=== Mochi's Tasks Only ===
  Morning walk           [high]
  Give medication        [high]
  Brushing               [low]

=== Pending Tasks Only ===
  Morning walk           [high]
  Brushing               [low]
  Feeding                [medium]

=== Completed Tasks ===
  Give medication        [done]
```
