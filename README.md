# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. PawPal+ tracks tasks and helps organize a daily schedule by:

- Recording scheduled times, durations, priorities, and recurrence.
- Sorting and filtering tasks for the daily schedule.
- Flagging unfinished tasks with identical start times.

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- Keep owner and pet data for the current Streamlit session.
- Add care tasks with a scheduled time, duration, frequency, and priority.
- Sort tasks by time, priority, or duration, and filter by pet and completion status.
- Create the next occurrence when a daily or weekly task is marked complete.
- Warn when unfinished tasks share an exact start time.
- Run a terminal demo and an automated test suite.

The final class diagram is in [`diagrams/uml_final.mmd`](diagrams/uml_final.mmd).

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Streamlit UI

From the project directory in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🧪 Testing PawPal+

The automated tests cover:

- Task completion and adding tasks to a pet.
- Sorting by time, priority, and duration, including stable ordering for ties.
- Filtering by pet and completion status.
- Daily and weekly recurrence, and no recurrence for as-needed tasks.
- Exact-time conflict warnings, invalid time formats, and an owner with no tasks.

From the project directory with its virtual environment activated, run:

```powershell
python -m pytest
```

On Windows PowerShell, you can run it without activating the environment:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Successful test run:

```text
============================= test session starts =============================
collected 12 items

tests\test_pawpal.py ............                                        [100%]

============================= 12 passed in 0.06s ==============================
```

**Confidence level:** ★★★★☆ (4/5). Core scheduler behaviors are covered; duration-overlap detection and broader UI behavior still need additional testing.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Time sorting | `Scheduler.sort_by_time` | Sorts by `HH:MM`; equal times preserve entry order. |
| Other sorting | `Scheduler.get_schedule(sort_by)` | Supports priority high-to-low and duration shortest-first. |
| Filtering | `Scheduler.filter_tasks` / `Scheduler.get_schedule` | Filters by pet, completion status, and due date. |
| Conflict handling | `Scheduler.detect_conflicts` | Warns about exact matching start times; duration overlap is not checked. |
| Recurring tasks | `Scheduler.mark_task_complete` | Creates the next daily (+1 day) or weekly (+7 days) occurrence; as-needed tasks do not recur. |

## Demo Walkthrough

1. Enter an owner name and add one or more pets.
2. Add a task for a pet with a scheduled time, duration, frequency, and priority.
3. Use the task list to mark a due task complete. Daily and weekly tasks create a next occurrence for one or seven days later.
4. Choose how to sort and filter the schedule, then select **Generate schedule**.
5. Review the schedule and any exact-start-time conflict warnings. Move one task to a different time to resolve a warning.

Run the terminal demo with `python main.py`. It shows time sorting, pet filtering, recurrence, and conflict detection:

```text
Today's Schedule (sorted by time)
- 08:00 | Medication for Mochi (5 min, daily) [priority: high]
- 08:00 | Feeding for Nori (10 min, daily) [priority: medium]
- 09:00 | Morning walk for Mochi (30 min, daily) [priority: high]

Mochi's unfinished tasks
- Morning walk
- Medication
Warning: Conflict at 08:00: Medication for Mochi, Feeding for Nori

Next medication due: 2026-11-14
```

The next-due date changes based on the date the demo is run.
