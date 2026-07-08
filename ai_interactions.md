# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to help build a complete pet care task scheduler from scratch — including UML design, Python class stubs, scheduling logic, test suite, Streamlit UI wiring, and algorithmic features like sorting, filtering, conflict detection, recurring tasks, and a next-available-slot finder.

**What did the agent do?**

- Created `pawpal_system.py` with `Task`, `Pet`, `Owner`, and `Scheduler` classes
- Implemented `generate_schedule()`, `sort_by_time()`, `filter_tasks()`, `get_conflicts()`, `mark_complete()`, `next_occurrence()`, and `find_next_slot()`
- Wrote 7 pytest tests in `tests/test_pawpal.py` covering happy paths and edge cases
- Wired the Streamlit UI in `app.py` to use session state and all Scheduler methods
- Updated `diagrams/uml.mmd` and created `diagrams/uml_final.mmd` to reflect the final class structure
- Filled in `reflection.md` and `README.md` throughout the build

**What did you have to verify or fix manually?**

When the agent suggested a more Pythonic version of `get_conflicts()` using `itertools.combinations` and a nested list comprehension, I reviewed both versions and kept the original. The Pythonic version was harder to read for a human skimming the code, which matters more here than saving two lines. I also reviewed every piece of code before it was written to the file, and approved or modified the preview before confirming.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
