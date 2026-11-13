from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(name="Jordan")
mochi = Pet(name="Mochi", species="dog")
nori = Pet(name="Nori", species="cat")

mochi.add_task(Task("Morning walk", 30, "daily"))
mochi.add_task(Task("Medication", 5, "daily"))
nori.add_task(Task("Feeding", 10, "daily"))

owner.add_pet(mochi)
owner.add_pet(nori)

scheduler = Scheduler()
print("Today's Schedule")
for pet, task in scheduler.get_schedule(owner):
    print(f"- {task.description} for {pet.name} ({task.duration_minutes} min, {task.frequency})")
