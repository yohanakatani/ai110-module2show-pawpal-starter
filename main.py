from tabulate import tabulate
from pawpal_system import Task, Pet, Owner, Scheduler

walk = Task("Morning walk", 30, "high", time="08:00")
meds = Task("Give medication", 10, "high", frequency="daily", time="07:00")
grooming = Task("Brushing", 20, "low", frequency="weekly", time="10:00")
feeding = Task("Feeding", 10, "medium", time="09:00")

mochi = Pet("Mochi", "dog")
mochi.add_task(walk)
mochi.add_task(meds)
mochi.add_task(grooming)

luna = Pet("Luna", "cat")
luna.add_task(feeding)

jordan = Owner("Jordan", available_minutes=60)
jordan.add_pet(mochi)
jordan.add_pet(luna)

scheduler = Scheduler(jordan)
result = scheduler.generate_schedule()

planned_titles = {t.title for t in result["planned"]}
skipped_titles = {t.title for t in result["skipped"]}

def status(task):
    if task.title in planned_titles:
        return "planned"
    elif task.title in skipped_titles:
        return "skipped"
    return "pending"

print(f"\nToday's Schedule -- {jordan.name} ({jordan.available_minutes} min available)\n")

rows = [
    [t.time, t.title, f"{t.duration_minutes} min", t.priority, t.frequency, status(t)]
    for t in scheduler.sort_by_priority_then_time()
]
print(tabulate(rows, headers=["Time", "Task", "Duration", "Priority", "Frequency", "Status"], tablefmt="simple"))

if result["skipped"]:
    print("\nSkipped (not enough time):")
    skipped_rows = [[t.title, f"{t.duration_minutes} min", t.priority] for t in result["skipped"]]
    print(tabulate(skipped_rows, headers=["Task", "Duration", "Priority"], tablefmt="simple"))

conflicts = scheduler.get_conflicts()
if conflicts:
    print("\nConflicts detected:")
    for c in conflicts:
        print(f"  WARNING: {c}")
