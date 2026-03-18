# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

_Three core actions the user should be able to perform: add a pet and owner, schedule a task like a walk, see today's tasks/schedule._

_I did 4 classes: Owner, Pet, Task, and Scheduler. Owner has a list of pets and an amount of available minutes per day. Pet has a name, species, owner, list of tasks for it, and the ability to add a task. Task has a title, duration, priority, and status, and tasks can be marked done. Scheduler is linked to an owner and can generate and explain today's plan._

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

_After AI feedback, tasks now have a pet id field to link them back to the pet, as well as a due date. Scheduler has a plan_reasons field now._

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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




### _Here's the initial mermaid diagram I had:_

``` classDiagram
class Owner {
+owner_id: int
+name: string
+available_minutes_per_day: int
+pets: listPet
+add_pet(pet: Pet)
+get_all_tasks(): listTask
}

class Pet {
+pet_id: int
+name: string
+species: string
+owner_id: int
+tasks: listTask
+add_task(task: Task)
+get_tasks_for_date(date): listTask
}

class Task {
+task_id: int
+title: string
+duration_minutes: int
+priority: int
+status: string
+mark_done()
}

class Scheduler {
+owner: Owner
+today_plan: listTask
+generate_daily_plan(date): listTask
+explain_plan(): string
}

Owner "1" --> "" Pet : owns
Pet "1" --> "" Task : has
Scheduler "1" --> "1" Owner : uses
Scheduler "1" --> "*" Task : schedules