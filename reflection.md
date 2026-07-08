# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Before writing any code, I thought about what a pet owner would actually
need to do with this app. I landed on three core actions:

1. **Add pet care tasks** — The owner can add tasks like "morning walk" or
   "give medication," along with how long each one takes and how important
   it is. Nothing fancy, just a simple way to build up a list of things
   that need to happen.

2. **Generate a daily schedule** — Once the tasks are in, the owner tells
   the app how much time they have, and the app puts together a plan for
   the day. It puts the most important tasks first and stops when time runs
   out.

3. **See the plan and understand it** — The schedule shows up as a clear
   list with times, so the owner knows exactly what to do and when. If
   something got left out because there wasn't enough time, the app says so,
   so there are no surprises.

**b. Design changes**

I removed an unused `field` import that snuck in by default. I also added
a return type to `generate_schedule()` so the UI knows what to expect —
a dict with a planned list and a skipped list.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: available time and task
priority. Priority came first because missing a high-priority task like
medication is worse than skipping a low-priority grooming session. Time
was second — the scheduler fills the day in priority order and stops when
time runs out. I didn't add preference-based filtering because the app
didn't need it to be useful.

**b. Tradeoffs**

The conflict detector only catches tasks at the exact same time. It won't
flag a 30-minute task at 08:00 and another at 08:15, even though they
overlap. It's a simplification, but for a pet care app it's good enough.

---

## 3. AI Collaboration

**a. How you used AI**

I used the AI assistant across every phase — drafting the UML, generating
class stubs, implementing scheduling logic, writing tests, and wiring the
UI. The most useful prompts were specific ones: asking for "a lightweight
conflict detection strategy that returns warnings instead of crashing" got
a much better result than asking for "conflict detection." Asking the AI
to show me the output before writing it to a file also saved a lot of
back-and-forth.

**b. Judgment and verification**

When the AI suggested a more Pythonic version of get_conflicts() using
itertools.combinations and a nested list comprehension, I looked at both
versions and kept the original. The Pythonic one was shorter but harder
to read at a glance. Since this is a learning project and readability
matters, that was the right call. I verified by reading both versions
side by side and asking which one a new reader would understand faster.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
