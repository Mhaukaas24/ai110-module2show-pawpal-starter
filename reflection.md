# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

1. Enter basic owner and pet information.
2. Add or edit pet-care tasks, including duration and priority.
3. Generate a daily care plan and see why each task was chosen.

**a. Initial design**

The initial UML uses four classes:

- `Owner` stores the owner's name, daily time availability, preferences, and pets.
- `Pet` stores a pet's name, species, and care tasks.
- `CareTask` describes a care activity, its duration, priority, and category.
- `DailyPlan` groups the tasks selected for one pet on one date and records why they were included.

An owner can have multiple pets, each pet can have multiple care tasks, and a daily plan is for one pet and can include multiple care tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler flags tasks with the same exact start time, but does not detect
overlapping durations. This keeps conflict detection simple, but could miss a
30-minute task at 08:00 overlapping a task at 08:15.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
