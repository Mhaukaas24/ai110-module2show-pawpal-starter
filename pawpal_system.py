from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str
    is_completed: bool = False

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
    def get_schedule(self, owner: Owner) -> list[tuple[Pet, Task]]:
        """Return unfinished tasks with their pets in entry order."""
        return [
            (pet, task)
            for pet in owner.pets
            for task in pet.tasks
            if not task.is_completed
        ]
