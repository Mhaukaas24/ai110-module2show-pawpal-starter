from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task("Give medication", 5, "daily")

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 30, "daily")

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_schedule_sorts_by_priority_with_entry_order_for_ties() -> None:
    pet = Pet("Mochi", "dog")
    high_first = Task("Morning walk", 30, "daily", priority="high")
    low = Task("Grooming", 20, "weekly", priority="low")
    high_second = Task("Medication", 5, "daily", priority="high")
    pet.add_task(high_first)
    pet.add_task(low)
    pet.add_task(high_second)
    owner = Owner("Jordan", pets=[pet])

    schedule = Scheduler().get_schedule(owner, sort_by="priority")

    assert schedule == [
        (pet, high_first),
        (pet, high_second),
        (pet, low),
    ]


def test_schedule_sorts_by_shortest_duration() -> None:
    pet = Pet("Mochi", "dog")
    long_task = Task("Walk", 30, "daily", priority="high")
    short_task = Task("Medication", 5, "daily", priority="low")
    medium_task = Task("Feeding", 10, "daily", priority="medium")
    pet.add_task(long_task)
    pet.add_task(short_task)
    pet.add_task(medium_task)
    owner = Owner("Jordan", pets=[pet])

    schedule = Scheduler().get_schedule(owner, sort_by="duration")

    assert schedule == [
        (pet, short_task),
        (pet, medium_task),
        (pet, long_task),
    ]


def test_schedule_sorts_by_time() -> None:
    pet = Pet("Mochi", "dog")
    late_task = Task("Walk", 30, "daily", time="09:30")
    early_task = Task("Medication", 5, "daily", time="08:00")
    pet.add_task(late_task)
    pet.add_task(early_task)
    owner = Owner("Jordan", pets=[pet])

    schedule = Scheduler().get_schedule(owner, sort_by="time")

    assert schedule == [(pet, early_task), (pet, late_task)]


def test_filter_tasks_by_pet_and_completion_status() -> None:
    mochi = Pet("Mochi", "dog")
    nori = Pet("Nori", "cat")
    pending = Task("Walk", 30, "daily")
    completed = Task("Medication", 5, "daily", is_completed=True)
    other_pet_task = Task("Feeding", 10, "daily")
    mochi.add_task(pending)
    mochi.add_task(completed)
    nori.add_task(other_pet_task)
    owner = Owner("Jordan", pets=[mochi, nori])

    assert Scheduler().filter_tasks(
        owner,
        pet_name="mochi",
        is_completed=False,
    ) == [(mochi, pending)]
    assert Scheduler().filter_tasks(owner, is_completed=True) == [
        (mochi, completed)
    ]


@pytest.mark.parametrize(
    ("frequency", "days_until_next"),
    [("daily", 1), ("weekly", 7)],
)
def test_completing_recurring_task_creates_next_occurrence(
    frequency: str,
    days_until_next: int,
) -> None:
    completed_on = date(2026, 11, 13)
    pet = Pet("Mochi", "dog")
    task = Task(
        "Medication",
        5,
        frequency,
        priority="high",
        time="08:30",
        due_date=completed_on,
    )
    pet.add_task(task)

    next_task = Scheduler().mark_task_complete(pet, task, completed_on)

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.due_date == completed_on + timedelta(days=days_until_next)
    assert next_task.time == task.time
    assert next_task.priority == task.priority
    assert next_task.is_completed is False
    assert pet.tasks == [task, next_task]


def test_completing_as_needed_task_does_not_create_an_occurrence() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Brush coat", 10, "as needed")
    pet.add_task(task)

    next_task = Scheduler().mark_task_complete(pet, task, date(2026, 11, 13))

    assert next_task is None
    assert task.is_completed is True
    assert pet.tasks == [task]


def test_detect_conflicts_for_matching_start_times() -> None:
    mochi = Pet("Mochi", "dog")
    nori = Pet("Nori", "cat")
    mochi.add_task(Task("Walk", 30, "daily", time="08:00"))
    nori.add_task(Task("Feeding", 10, "daily", time="08:00"))
    nori.add_task(Task("Grooming", 60, "weekly", time="08:15"))
    owner = Owner("Jordan", pets=[mochi, nori])
    scheduler = Scheduler()
    schedule = scheduler.get_schedule(owner, sort_by="time")

    conflicts = scheduler.detect_conflicts(schedule)

    assert conflicts == [
        "Conflict at 08:00: Walk for Mochi, Feeding for Nori"
    ]


def test_task_rejects_non_hhmm_time() -> None:
    with pytest.raises(ValueError, match="HH:MM"):
        Task("Walk", 30, "daily", time="8:00")
