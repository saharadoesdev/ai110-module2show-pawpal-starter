from datetime import date, datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_data() -> Scheduler:
	owner = Owner(owner_id=1, name="Sahara", available_minutes_per_day=180)

	pet_one = Pet(pet_id=101, name="Milo", species="Dog", owner_id=owner.owner_id)
	pet_two = Pet(pet_id=102, name="Luna", species="Cat", owner_id=owner.owner_id)

	today = date.today()

	task_walk = Task(
		task_id=1,
		pet_id=pet_one.pet_id,
		description="Morning walk",
		scheduled_for=datetime(today.year, today.month, today.day, 8, 0),
		frequency="once",
		duration_minutes=30,
		priority=3,
	)
	task_feed = Task(
		task_id=2,
		pet_id=pet_two.pet_id,
		description="Feed dinner",
		scheduled_for=datetime(today.year, today.month, today.day, 18, 0),
		frequency="once",
		duration_minutes=15,
		priority=2,
	)
	task_meds = Task(
		task_id=3,
		pet_id=pet_one.pet_id,
		description="Give medication",
		scheduled_for=datetime(today.year, today.month, today.day, 21, 0),
		frequency="once",
		duration_minutes=10,
		priority=5,
	)

	pet_one.add_task(task_walk)
	pet_one.add_task(task_meds)
	pet_two.add_task(task_feed)

	owner.add_pet(pet_one)
	owner.add_pet(pet_two)

	return Scheduler(owner)


def print_todays_schedule(scheduler: Scheduler) -> None:
	today = date.today()
	plan = scheduler.generate_daily_plan(today)

	print("Today's Schedule")
	print("-" * 16)

	if not plan:
		print("No tasks scheduled for today.")
		return

	for task in plan:
		time_text = task.scheduled_for.strftime("%I:%M %p") if task.scheduled_for else "No time"
		print(f"{time_text} | Pet #{task.pet_id} | {task.description} (Priority {task.priority})")


if __name__ == "__main__":
	scheduler = build_demo_data()
	print_todays_schedule(scheduler)
