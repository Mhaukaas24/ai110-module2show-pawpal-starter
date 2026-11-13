# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

1. Enter owner and pet information.
2. Add pet-care tasks with a scheduled time, duration, frequency, and priority.
3. Generate a daily schedule, sort and filter it, and mark due tasks complete.

**a. Initial design**

The initial UML uses four classes:

- `Owner` stores the owner's name, daily time availability, preferences, and pets.
- `Pet` stores a pet's name, species, and care tasks.
- `CareTask` describes a care activity, its duration, priority, and category.
- `DailyPlan` groups the tasks selected for one pet on one date and records why they were included.

An owner can have multiple pets, each pet can have multiple care tasks, and a daily plan is for one pet and can include multiple care tasks.

**b. Design changes**

The initial UML used `CareTask` and `DailyPlan`. During implementation, I followed
the Phase 2 model of `Task`, `Pet`, `Owner`, and `Scheduler`. The final model
stores tasks on each pet, while `Scheduler` handles sorting, filtering,
recurrence, and conflict detection instead of storing a separate `DailyPlan`.
The task model was extended with scheduled time, due date, and priority to
support the later scheduling and UI requirements.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler includes tasks due on or before the selected date, and can filter
by pet and completion status. It can sort by scheduled time, priority
(high-to-low), or duration (shortest-first). Priority and duration affect order;
the scheduler does not optimize around owner availability or preferences.

**b. Tradeoffs**

The scheduler flags tasks with the same exact start time, but does not detect
overlapping durations. This keeps conflict detection simple, but could miss a
30-minute task at 08:00 overlapping a task at 08:15.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to help with coding and testing. A clear feature request, such as
adding priority to tasks and enabling schedules to sort by priority or duration,
helped guide the implementation. I kept the phases in one conversation, which
was useful because earlier design and feature decisions stayed in context.

**b. Judgment and verification**

The initial implementation did not include a priority field, so I pointed out
the gap and prompted AI to add it. I checked the result with the priority-sorting
tests and planned to try the UI before committing.

---

## 4. Testing and Verification

**a. What you tested**

The 12 automated tests cover task completion and adding tasks, sorting by time,
priority, and duration (including ties), filtering by pet and completion status,
daily and weekly recurrence, non-recurring as-needed tasks, exact-time conflict
warnings, invalid time formats, and an owner with no tasks. These cases check
the main scheduler behaviors and important boundary conditions.

**b. Confidence**

I am 4/5 confident that the core scheduler behaviors work correctly. I would
next test duration-overlap detection and broader UI interactions, including
combinations of schedule filters and recurring-task completion.

---

## 5. Reflection

**a. What went well**

I am most satisfied with having a basic working prototype.

**b. What you would improve**

In another iteration, I would make the UI more intuitive.

**c. Key takeaway**

I learned that making design choices early makes it easier to avoid larger
changes later in implementation.
