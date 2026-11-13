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

## 🖥️ Sample Output

The terminal demo shows time sorting, pet filtering, recurrence, and conflict detection:

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

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Time sorting | `Scheduler.sort_by_time` | Sorts by `HH:MM`; equal times preserve entry order. |
| Other sorting | `Scheduler.get_schedule(sort_by)` | Supports priority high-to-low and duration shortest-first. |
| Filtering | `Scheduler.filter_tasks` / `Scheduler.get_schedule` | Filters by pet, completion status, and due date. |
| Conflict handling | `Scheduler.detect_conflicts` | Warns about exact matching start times; duration overlap is not checked. |
| Recurring tasks | `Scheduler.mark_task_complete` | Creates the next daily (+1 day) or weekly (+7 days) occurrence; as-needed tasks do not recur. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
