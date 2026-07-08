import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# --- Owner & Pet Setup ---
st.subheader("Owner & Pet Info")
col1, col2, col3, col4 = st.columns(4)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
with col3:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col4:
    available_minutes = st.number_input("Time available (min)", min_value=10, max_value=480, value=60)

if st.button("Set up owner & pet"):
    pet = Pet(name=pet_name, species=species)
    owner = Owner(name=owner_name, available_minutes=available_minutes)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.scheduler = Scheduler(owner)
    st.success(f"Owner {owner_name} and pet {pet_name} set up!")

st.divider()

# --- Add Tasks ---
st.subheader("Add Tasks")
if st.session_state.owner is None:
    st.info("Set up your owner and pet first.")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col5:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add task"):
        task = Task(title=task_title, duration_minutes=int(duration),
                    priority=priority, time=task_time, frequency=frequency)
        st.session_state.owner.pets[0].add_task(task)
        st.success(f"Added: {task_title}")

    all_tasks = st.session_state.scheduler.sort_by_time()
    if all_tasks:
        st.write("Current tasks (sorted by time):")
        st.table([{
            "title": t.title,
            "time": t.time,
            "duration": t.duration_minutes,
            "priority": t.priority,
            "frequency": t.frequency
        } for t in all_tasks])

        conflicts = st.session_state.scheduler.get_conflicts()
        if conflicts:
            for c in conflicts:
                st.warning(f"⚠️ {c}")
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Schedule")
if st.button("Generate schedule"):
    if st.session_state.scheduler is None:
        st.warning("Set up your owner and pet first.")
    else:
        result = st.session_state.scheduler.generate_schedule()
        st.markdown(f"**Today's plan for {st.session_state.owner.name}** ({st.session_state.owner.available_minutes} min available)")

        if result["planned"]:
            st.markdown("**Planned:**")
            for task in result["planned"]:
                st.success(f"{task.time} — {task.title} ({task.duration_minutes} min) [{task.priority}]")
        if result["skipped"]:
            st.markdown("**Skipped (not enough time):**")
            for task in result["skipped"]:
                st.warning(f"{task.title} ({task.duration_minutes} min) [{task.priority}]")
