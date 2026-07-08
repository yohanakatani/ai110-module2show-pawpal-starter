from pawpal_system import Task, Pet, Owner, Scheduler

walk = Task("Morning walk", 30, "high", time="08:00")
meds = Task("Give medication", 10, "high", frequency="daily", time="08:00")  # same time as walk
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

print("=== Conflict Detection ===")
conflicts = scheduler.get_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")
