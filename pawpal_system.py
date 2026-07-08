from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List
import json


@dataclass
class Task:
    """A single pet care activity."""
    title: str
    duration_minutes: int
    priority: str
    frequency: str = "daily"
    completed: bool = False
    time: str = "00:00"
    due_date: date = field(default_factory=date.today)

    def complete(self):
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> "Task":
        """Return a new Task scheduled for the next occurrence based on frequency."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None
        return Task(self.title, self.duration_minutes, self.priority,
                    self.frequency, completed=False, time=self.time, due_date=next_date)

    def __repr__(self):
        """Return a readable string representation of the task."""
        status = "done" if self.completed else "pending"
        return f"{self.title} ({self.duration_minutes}min, {self.priority}, {status})"


@dataclass
class Pet:
    """Stores pet details and its task list."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_pending(self) -> List[Task]:
        """Return all tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]

    def get_completed(self) -> List[Task]:
        """Return all tasks that have been completed."""
        return [t for t in self.tasks if t.completed]


@dataclass
class Owner:
    """Manages the owner and their pets."""
    name: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
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

    def sort_by_time(self) -> List[Task]:
        """Return all pending tasks sorted by scheduled time (HH:MM)."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.time)

    def mark_complete(self, title: str):
        """Mark a task complete and auto-schedule the next occurrence if recurring."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.title == title and not task.completed:
                    task.complete()
                    next_task = task.next_occurrence()
                    if next_task:
                        pet.add_task(next_task)
                    return

    def get_conflicts(self) -> List[str]:
        """Return warning messages for tasks scheduled at the same time."""
        seen = {}
        warnings = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                if not task.completed:
                    key = task.time
                    if key in seen:
                        warnings.append(
                            f"Conflict at {task.time}: '{task.title}' ({pet.name}) "
                            f"clashes with '{seen[key][0]}' ({seen[key][1]})"
                        )
                    else:
                        seen[key] = (task.title, pet.name)
        return warnings

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name:
            tasks = [t for pet in self.owner.pets if pet.name == pet_name for t in pet.tasks]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def find_next_slot(self, duration_minutes: int) -> str:
        """Return the earliest HH:MM slot that doesn't conflict with existing tasks."""
        booked = {t.time for pet in self.owner.pets for t in pet.tasks if not t.completed}
        hour, minute = 7, 0
        while hour < 21:
            slot = f"{hour:02d}:{minute:02d}"
            if slot not in booked:
                return slot
            minute += duration_minutes
            if minute >= 60:
                hour += minute // 60
                minute = minute % 60
        return "No available slot found"

    def save_to_json(self, filepath: str):
        """Serialize the owner, pets, and tasks to a JSON file."""
        data = {
            "owner": {
                "name": self.owner.name,
                "available_minutes": self.owner.available_minutes,
                "pets": [
                    {
                        "name": pet.name,
                        "species": pet.species,
                        "tasks": [
                            {
                                "title": t.title,
                                "duration_minutes": t.duration_minutes,
                                "priority": t.priority,
                                "frequency": t.frequency,
                                "completed": t.completed,
                                "time": t.time,
                                "due_date": t.due_date.isoformat(),
                            }
                            for t in pet.tasks
                        ],
                    }
                    for pet in self.owner.pets
                ],
            }
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_json(cls, filepath: str) -> "Scheduler":
        """Reconstruct a Scheduler from a JSON file."""
        with open(filepath) as f:
            data = json.load(f)
        o = data["owner"]
        owner = Owner(name=o["name"], available_minutes=o["available_minutes"])
        for p in o["pets"]:
            pet = Pet(name=p["name"], species=p["species"])
            for t in p["tasks"]:
                pet.add_task(Task(
                    title=t["title"],
                    duration_minutes=t["duration_minutes"],
                    priority=t["priority"],
                    frequency=t["frequency"],
                    completed=t["completed"],
                    time=t["time"],
                    due_date=date.fromisoformat(t["due_date"]),
                ))
            owner.add_pet(pet)
        return cls(owner)

    def daily_summary(self) -> str:
        """Return a formatted string of all pending tasks grouped by pet."""
        lines = [f"Daily plan for {self.owner.name}:"]
        for pet in self.owner.pets:
            lines.append(f"\n  {pet.name} ({pet.species}):")
            for task in pet.get_pending():
                lines.append(f"    - {task}")
        return "\n".join(lines)
