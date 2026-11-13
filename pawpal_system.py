from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Literal


Priority = Literal["low", "medium", "high"]
SortBy = Literal["time", "priority", "duration"]
_PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str
    is_completed: bool = False
    priority: Priority = "medium"
    time: str = "09:00"
    due_date: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        if self.priority not in _PRIORITY_RANK:
            raise ValueError("priority must be 'low', 'medium', or 'high'")
        try:
            parsed_time = datetime.strptime(self.time, "%H:%M")
        except (TypeError, ValueError) as exc:
            raise ValueError("time must use HH:MM format") from exc
        if parsed_time.strftime("%H:%M") != self.time:
            raise ValueError("time must use HH:MM format")

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks belonging to the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def filter_tasks(
        self,
        owner: Owner,
        pet_name: str | None = None,
        is_completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter tasks by pet name and completion status."""
        normalized_pet_name = pet_name.casefold() if pet_name is not None else None
        return [
            (pet, task)
            for pet in owner.pets
            if normalized_pet_name is None
            or pet.name.casefold() == normalized_pet_name
            for task in pet.tasks
            if is_completed is None or task.is_completed == is_completed
        ]

    def sort_by_time(
        self,
        schedule: list[tuple[Pet, Task]],
    ) -> list[tuple[Pet, Task]]:
        """Return scheduled tasks in ascending HH:MM order."""
        return sorted(schedule, key=lambda item: item[1].time)

    def get_schedule(
        self,
        owner: Owner,
        sort_by: SortBy = "time",
        pet_name: str | None = None,
        is_completed: bool | None = False,
        on_date: date | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Return due tasks filtered by pet and status, in the chosen order."""
        schedule_date = on_date or date.today()
        schedule = [
            (pet, task)
            for pet, task in self.filter_tasks(owner, pet_name, is_completed)
            if task.due_date <= schedule_date
        ]
        if sort_by == "time":
            return self.sort_by_time(schedule)
        if sort_by == "priority":
            schedule.sort(key=lambda item: _PRIORITY_RANK[item[1].priority])
        elif sort_by == "duration":
            schedule.sort(key=lambda item: item[1].duration_minutes)
        else:
            raise ValueError("sort_by must be 'time', 'priority', or 'duration'")
        return schedule

    def mark_task_complete(
        self,
        pet: Pet,
        task: Task,
        completed_on: date | None = None,
    ) -> Task | None:
        """Complete a task and add its next daily or weekly occurrence."""
        if not any(existing is task for existing in pet.tasks):
            raise ValueError("task does not belong to this pet")
        if task.is_completed:
            return None

        task.mark_complete()
        recurrence_days = {"daily": 1, "weekly": 7}.get(task.frequency)
        if recurrence_days is None:
            return None

        next_task = Task(
            description=task.description,
            duration_minutes=task.duration_minutes,
            frequency=task.frequency,
            priority=task.priority,
            time=task.time,
            due_date=(completed_on or date.today()) + timedelta(days=recurrence_days),
        )
        pet.add_task(next_task)
        return next_task

    def detect_conflicts(self, schedule: list[tuple[Pet, Task]]) -> list[str]:
        """Return warnings for tasks with matching start times."""
        tasks_by_time: dict[str, list[str]] = {}
        for pet, task in schedule:
            tasks_by_time.setdefault(task.time, []).append(
                f"{task.description} for {pet.name}"
            )
        return [
            f"Conflict at {scheduled_time}: {', '.join(descriptions)}"
            for scheduled_time, descriptions in tasks_by_time.items()
            if len(descriptions) > 1
        ]
