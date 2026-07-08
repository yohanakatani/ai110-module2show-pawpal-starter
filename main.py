from pawpal_system import Task, Pet, Owner, Scheduler

walk = Task("Morning walk", 30, "high")
meds = Task("Give medication", 10, "high")
grooming = Task("Brushing", 20, "low", frequency="weekly")
feeding = Task("Feeding", 10, "medium")

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

print(f"Today's Schedule — {jordan.name} ({jordan.available_minutes} min available)")
for pet in jordan.pets:
    print(f"\n{pet.name} ({pet.species})")
    for task in pet.get_pending():
        print(f"  {task.title:<22} {task.duration_minutes} min   {task.priority}")

if result["skipped"]:
    print("\nSkipped (not enough time):")
    for task in result["skipped"]:
        print(f"  {task.title:<22} {task.duration_minutes} min   {task.priority}")
