from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    walk = Task("Morning walk", 30, "high")
    mochi = Pet("Mochi", "dog")
    mochi.add_task(walk)

    owner = Owner("Jordan", available_minutes=60)
    owner.add_pet(mochi)

    scheduler = Scheduler(owner)
    scheduler.mark_complete("Morning walk")

    assert walk.completed is True


def test_add_task_increases_count():
    mochi = Pet("Mochi", "dog")
    assert len(mochi.tasks) == 0

    mochi.add_task(Task("Morning walk", 30, "high"))
    mochi.add_task(Task("Feeding", 10, "medium"))

    assert len(mochi.tasks) == 2
