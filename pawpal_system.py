from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str
    category: str = "general"


@dataclass
class Pet:
    name: str
    species: str
    care_tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        raise NotImplementedError

    def remove_task(self, task: CareTask) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def update_preferences(self, preferences: list[str]) -> None:
        raise NotImplementedError


@dataclass
class DailyPlan:
    plan_date: date
    pet: Pet
    scheduled_tasks: list[CareTask] = field(default_factory=list)
    explanations: dict[str, str] = field(default_factory=dict)

    def total_duration(self) -> int:
        raise NotImplementedError

    def explain(self) -> str:
        raise NotImplementedError
