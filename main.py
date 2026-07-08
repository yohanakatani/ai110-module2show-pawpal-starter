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

print("=== Today's Schedule ===")
print(scheduler.daily_summary())
print("\nPlanned tasks:", result["planned"])
print("Skipped tasks:", result["skipped"])
