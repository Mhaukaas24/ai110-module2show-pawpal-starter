from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name="Jordan")
owner: Owner = st.session_state["owner"]

if "owner_name" not in st.session_state:
    st.session_state["owner_name"] = owner.name
if "show_schedule" not in st.session_state:
    st.session_state["show_schedule"] = False

scheduler = Scheduler()
for pet in owner.pets:
    for task in pet.tasks:
        if not hasattr(task, "priority"):
            task.priority = "medium"
        if not hasattr(task, "time"):
            task.time = "09:00"
        if not hasattr(task, "due_date"):
            task.due_date = date.today()

owner.name = st.text_input("Owner name", key="owner_name")

st.title("🐾 PawPal+")
st.markdown(
    "Manage your pets' care tasks, mark completed tasks, and generate a list "
    "of the unfinished activities."
)

with st.expander("About PawPal+", expanded=False):
    st.markdown(
        """
PawPal+ helps pet owners keep track of care activities. Each task records its
scheduled time, duration, frequency, and priority. The scheduler can sort and
filter tasks, create daily and weekly recurrences, and warn about exact-time conflicts.
"""
    )

st.divider()
st.subheader("Add a pet")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name_input = st.text_input("Pet name")
    species_input = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name_input.strip():
        st.error("Enter a pet name.")
    else:
        owner.add_pet(Pet(name=pet_name_input.strip(), species=species_input))
        st.success(f"Added {pet_name_input.strip()}.")

st.divider()
st.subheader("Add a care task")

if not owner.pets:
    st.info("Add a pet before adding tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_index = st.selectbox(
            "Pet",
            options=range(len(owner.pets)),
            format_func=lambda index: (
                f"{owner.pets[index].name} ({owner.pets[index].species}) "
                f"— pet {index + 1}"
            ),
        )
        task_description = st.text_input("Task description", value="Morning walk")
        task_time = st.time_input("Scheduled time", value=time(9, 0))
        duration_minutes = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if not task_description.strip():
            st.error("Enter a task description.")
        else:
            owner.pets[pet_index].add_task(
                Task(
                    description=task_description.strip(),
                    duration_minutes=int(duration_minutes),
                    frequency=frequency,
                    priority=priority,
                    time=task_time.strftime("%H:%M"),
                    due_date=date.today(),
                )
            )
            st.success(f"Added task for {owner.pets[pet_index].name}.")

st.divider()
st.subheader("Your pets and tasks")

if not owner.pets:
    st.info("No pets yet.")
else:
    for pet_index, pet in enumerate(owner.pets):
        st.markdown(f"**{pet.name} ({pet.species})**")
        if not pet.tasks:
            st.caption("No tasks yet.")
            continue

        for task_index, task in enumerate(pet.tasks):
            task_columns = st.columns([1, 3, 1, 1, 1, 1.4, 1.2])
            task_columns[0].write(task.time)
            task_columns[1].write(task.description)
            task_columns[2].write(f"{task.duration_minutes} min")
            task_columns[3].write(task.frequency)
            task_columns[4].write(task.priority.title())
            task_columns[5].write(task.due_date.isoformat())
            if task.is_completed:
                task_columns[6].write("Complete")
            elif task.due_date > date.today():
                task_columns[6].write("Upcoming")
            elif task_columns[6].button(
                "Complete",
                key=f"complete_{pet_index}_{task_index}",
            ):
                scheduler.mark_task_complete(pet, task)
                st.rerun()

st.divider()
st.subheader("Today's Schedule")
st.caption("Tasks due today or earlier; equal sort values preserve entry order.")
sort_labels = {
    "time": "Time (earliest first)",
    "priority": "Priority (high to low)",
    "duration": "Duration (shortest first)",
}
sort_by = st.selectbox(
    "Sort by",
    options=list(sort_labels),
    format_func=lambda option: sort_labels[option],
    key="schedule_sort",
)
pet_filter_options = [-1, *range(len(owner.pets))]
pet_filter = st.selectbox(
    "Filter by pet",
    options=pet_filter_options,
    format_func=lambda index: (
        "All pets"
        if index == -1
        else f"{owner.pets[index].name} — pet {index + 1}"
    ),
    key="schedule_pet_filter",
)
status_labels = {
    "Unfinished": False,
    "Completed": True,
    "All": None,
}
status_label = st.selectbox(
    "Filter by status",
    options=list(status_labels),
    key="schedule_status_filter",
)

if st.button("Generate schedule", type="primary"):
    st.session_state["show_schedule"] = True

if st.session_state["show_schedule"]:
    pet_name = owner.pets[pet_filter].name if pet_filter >= 0 else None
    schedule = scheduler.get_schedule(
        owner,
        sort_by=sort_by,
        pet_name=pet_name,
        is_completed=status_labels[status_label],
    )
    if not schedule:
        st.info("No tasks match the selected date and filters.")
    else:
        for pet, task in schedule:
            st.write(
                f"- {task.time} — {task.description} for {pet.name} "
                f"({task.duration_minutes} min, {task.frequency}, due {task.due_date}) "
                f"[priority: {task.priority}]"
            )
    if status_labels[status_label] is not True:
        pending_schedule = scheduler.get_schedule(
            owner,
            sort_by="time",
            pet_name=pet_name,
            is_completed=False,
        )
        for warning in scheduler.detect_conflicts(pending_schedule):
            st.warning(warning)
