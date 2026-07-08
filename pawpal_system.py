from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents a single pet care task."""
    title: str
    duration_minutes: int
    priority: str


@dataclass
class Owner:
    """Represents the pet owner and their pet's basic info."""
    name: str
    pet_name: str
    species: str
    available_minutes: int


class Scheduler:
    """Generates a daily care schedule based on the owner's tasks and time budget."""

    def __init__(self, owner: Owner, tasks: List[Task]):
        self.owner = owner
        self.tasks = tasks

    def generate_schedule(self):
        pass
