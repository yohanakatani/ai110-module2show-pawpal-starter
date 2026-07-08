from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """A single pet care activity."""
    title: str
    duration_minutes: int
    priority: str
    frequency: str = "daily"
    completed: bool = False

    def complete(self):
        self.completed = True

    def __repr__(self):
        status = "done" if self.completed else "pending"
        return f"{self.title} ({self.duration_minutes}min, {self.priority}, {status})"


@dataclass
class Pet:
    """Stores pet details and its task list."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_pending(self) -> List[Task]:
        return [t for t in self.tasks if not t.completed]

    def get_completed(self) -> List[Task]:
        return [t for t in self.tasks if t.completed]


@dataclass
class Owner:
    """Manages the owner and their pets."""
    name: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Organizes and manages tasks across all pets."""

    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> dict:
        """Returns {"planned": [Task, ...], "skipped": [Task, ...]}"""
        pending = sorted(
            self.owner.get_all_tasks(),
            key=lambda t: self.PRIORITY_ORDER.get(t.priority, 99)
        )
        planned, skipped = [], []
        time_left = self.owner.available_minutes
        for task in pending:
            if not task.completed and task.duration_minutes <= time_left:
                planned.append(task)
                time_left -= task.duration_minutes
            else:
                skipped.append(task)
        return {"planned": planned, "skipped": skipped}

    def mark_complete(self, title: str):
        for task in self.owner.get_all_tasks():
            if task.title == title:
                task.complete()
                return

    def daily_summary(self) -> str:
        lines = [f"Daily plan for {self.owner.name}:"]
        for pet in self.owner.pets:
            lines.append(f"\n  {pet.name} ({pet.species}):")
            for task in pet.get_pending():
                lines.append(f"    - {task}")
        return "\n".join(lines)
