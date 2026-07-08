from pawpal_system import Task, Pet, Owner, Scheduler

# Tasks added out of order by time
walk = Task("Morning walk", 30, "high", time="08:00")
meds = Task("Give medication", 10, "high", time="07:00")
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

print("=== Sorted by Time ===")
for task in scheduler.sort_by_time():
    print(f"  {task.time}  {task.title:<22} {task.duration_minutes} min  [{task.priority}]")

print("\n=== Mochi's Tasks Only ===")
for task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {task.title:<22} [{task.priority}]")

meds.complete()

print("\n=== Pending Tasks Only ===")
for task in scheduler.filter_tasks(completed=False):
    print(f"  {task.title:<22} [{task.priority}]")

print("\n=== Completed Tasks ===")
for task in scheduler.filter_tasks(completed=True):
    print(f"  {task.title:<22} [done]")
