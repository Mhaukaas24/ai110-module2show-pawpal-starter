from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(name="Jordan")
mochi = Pet(name="Mochi", species="dog")
nori = Pet(name="Nori", species="cat")

morning_walk = Task(
    "Morning walk",
    30,
    "daily",
    priority="high",
    time="09:00",
)
medication = Task(
    "Medication",
    5,
    "daily",
    priority="high",
    time="08:00",
)
feeding = Task(
    "Feeding",
    10,
    "daily",
    priority="medium",
    time="08:00",
)
mochi.add_task(morning_walk)
mochi.add_task(medication)
nori.add_task(feeding)

owner.add_pet(mochi)
owner.add_pet(nori)

scheduler = Scheduler()
schedule = scheduler.get_schedule(owner, sort_by="time")
print("Today's Schedule (sorted by time)")
for pet, task in schedule:
    print(
        f"- {task.time} | {task.description} for {pet.name} "
        f"({task.duration_minutes} min, {task.frequency}) "
        f"[priority: {task.priority}]"
    )

print("\nMochi's unfinished tasks")
for pet, task in scheduler.filter_tasks(
    owner,
    pet_name="Mochi",
    is_completed=False,
):
    print(f"- {task.description}")

for warning in scheduler.detect_conflicts(schedule):
    print(f"Warning: {warning}")

next_medication = scheduler.mark_task_complete(
    mochi,
    medication,
    completed_on=date.today(),
)
if next_medication is not None:
    print(f"\nNext medication due: {next_medication.due_date}")
