from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def make_scheduler(available_minutes=60):
    walk = Task("Morning walk", 30, "high", time="08:00")
    meds = Task("Give medication", 10, "high", time="07:00")
    feeding = Task("Feeding", 10, "low", time="09:00")
    mochi = Pet("Mochi", "dog")
    mochi.add_task(walk)
    mochi.add_task(meds)
    mochi.add_task(feeding)
    owner = Owner("Jordan", available_minutes=available_minutes)
    owner.add_pet(mochi)
    return Scheduler(owner)


def test_high_priority_tasks_planned_first():
    scheduler = make_scheduler(available_minutes=40)
    result = scheduler.generate_schedule()
    planned_titles = [t.title for t in result["planned"]]
    assert planned_titles[0] in ["Morning walk", "Give medication"]
    assert "Feeding" in [t.title for t in result["skipped"]]


def test_sort_by_time_returns_chronological_order():
    scheduler = make_scheduler()
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_completing_daily_task_creates_next_occurrence():
    scheduler = make_scheduler()
    today = date.today()
    scheduler.mark_complete("Give medication")
    titles = [t.title for t in scheduler.owner.get_all_tasks()]
    assert titles.count("Give medication") == 2
    new_task = [t for t in scheduler.owner.get_all_tasks()
                if t.title == "Give medication" and not t.completed][0]
    assert new_task.due_date == today + timedelta(days=1)


def test_generate_schedule_with_no_tasks():
    owner = Owner("Jordan", available_minutes=60)
    owner.add_pet(Pet("Mochi", "dog"))
    scheduler = Scheduler(owner)
    result = scheduler.generate_schedule()
    assert result["planned"] == []
    assert result["skipped"] == []


def test_get_conflicts_detects_same_time():
    owner = Owner("Jordan", available_minutes=60)
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Morning walk", 30, "high", time="08:00"))
    pet.add_task(Task("Give medication", 10, "high", time="08:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    assert len(scheduler.get_conflicts()) == 1


def test_get_conflicts_no_conflicts():
    scheduler = make_scheduler()
    assert scheduler.get_conflicts() == []


def test_once_task_does_not_recur():
    owner = Owner("Jordan", available_minutes=60)
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Vet visit", 60, "high", frequency="once"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.mark_complete("Vet visit")
    assert len(owner.get_all_tasks()) == 1
