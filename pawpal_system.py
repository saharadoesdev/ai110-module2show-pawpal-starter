from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Task:
	task_id: int
	pet_id: int
	description: str
	scheduled_for: datetime | None = None
	frequency: str = "once"
	is_completed: bool = False
	duration_minutes: int = 0
	priority: int = 1

	def mark_done(self) -> None:
		"""Mark this task as completed."""
		self.is_completed = True

	def mark_pending(self) -> None:  # Optional helper (not required for MVP)
		"""Mark this task as not completed."""
		self.is_completed = False

	def is_due_on(self, target_date: date) -> bool:  # Optional helper used by should_run_on
		"""Return True if this task is scheduled exactly on target_date."""
		if self.scheduled_for is None:
			return False
		return self.scheduled_for.date() == target_date

	def should_run_on(self, target_date: date) -> bool:
		"""Return True when this task should be included on target_date."""
		if self.frequency == "daily":
			if self.scheduled_for is None:
				return True
			return self.scheduled_for.date() <= target_date
		if self.frequency == "weekly":
			if self.scheduled_for is None:
				return False
			return self.scheduled_for.weekday() == target_date.weekday() and self.scheduled_for.date() <= target_date
		return self.is_due_on(target_date)


@dataclass
class Pet:
	pet_id: int
	name: str
	species: str
	owner_id: int
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet after validating ownership and uniqueness."""
		if task.pet_id != self.pet_id:
			raise ValueError("Task pet_id does not match this pet")
		if any(existing.task_id == task.task_id for existing in self.tasks):
			raise ValueError("Task with this task_id already exists for this pet")
		self.tasks.append(task)

	def remove_task(self, task_id: int) -> bool:  # Optional helper (not required for MVP)
		"""Remove a task by id and return True when removed."""
		for index, task in enumerate(self.tasks):
			if task.task_id == task_id:
				self.tasks.pop(index)
				return True
		return False

	def get_tasks_for_date(self, target_date: date) -> list[Task]:
		"""Return this pet's tasks that should run on target_date."""
		return [task for task in self.tasks if task.should_run_on(target_date)]

	def get_pending_tasks(self) -> list[Task]:  # Optional helper (not required for MVP)
		"""Return this pet's tasks that are not completed."""
		return [task for task in self.tasks if not task.is_completed]


class Owner:
	def __init__(self, owner_id: int, name: str, available_minutes_per_day: int) -> None:
		"""Initialize an owner profile with daily time capacity."""
		self.owner_id = owner_id
		self.name = name
		self.available_minutes_per_day = available_minutes_per_day
		self.pets: list[Pet] = []

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner after validating ownership and uniqueness."""
		if pet.owner_id != self.owner_id:
			raise ValueError("Pet owner_id does not match this owner")
		if any(existing.pet_id == pet.pet_id for existing in self.pets):
			raise ValueError("Pet with this pet_id already exists")
		self.pets.append(pet)

	def remove_pet(self, pet_id: int) -> bool:  # Optional helper (not required for MVP)
		"""Remove a pet by id and return True when removed."""
		for index, pet in enumerate(self.pets):
			if pet.pet_id == pet_id:
				self.pets.pop(index)
				return True
		return False

	def get_pet(self, pet_id: int) -> Pet | None:  # Optional helper (not required for MVP)
		"""Return a pet by id, or None when it is not found."""
		for pet in self.pets:
			if pet.pet_id == pet_id:
				return pet
		return None

	def get_all_tasks(self) -> list[Task]:
		"""Return all tasks across all pets owned by this owner."""
		all_tasks: list[Task] = []
		for pet in self.pets:
			all_tasks.extend(pet.tasks)
		return all_tasks


class Scheduler:
	def __init__(self, owner: Owner) -> None:
		"""Initialize a scheduler bound to a specific owner."""
		self.owner = owner
		self.today_plan: list[Task] = []
		self.plan_reasons: dict[int, str] = {}

	def retrieve_all_tasks(self) -> list[Task]:  # Optional helper to keep logic modular
		"""Return all tasks available to this scheduler's owner."""
		return self.owner.get_all_tasks()

	def get_tasks_for_date(self, target_date: date, include_completed: bool = False) -> list[Task]:  # Optional helper for plan generation
		"""Return tasks scheduled for target_date with optional completed filtering."""
		tasks = [task for task in self.retrieve_all_tasks() if task.should_run_on(target_date)]
		if include_completed:
			return tasks
		return [task for task in tasks if not task.is_completed]

	def organize_tasks(self, tasks: list[Task]) -> list[Task]:  # Optional helper for sorting strategy
		"""Sort tasks by completion, scheduled time, priority, then task id."""
		def sort_key(task: Task) -> tuple[int, datetime, int, int]:
			scheduled = task.scheduled_for or datetime.max
			completion_rank = 1 if task.is_completed else 0
			return (completion_rank, scheduled, -task.priority, task.task_id)

		return sorted(tasks, key=sort_key)

	def generate_daily_plan(self, target_date: date) -> list[Task]:
		"""Generate and store the ordered task plan for target_date."""
		tasks_for_day = self.get_tasks_for_date(target_date, include_completed=False)
		ordered_tasks = self.organize_tasks(tasks_for_day)

		self.today_plan = ordered_tasks
		self.plan_reasons = {
			task.task_id: (
				"Included because it is due today"
				if task.frequency == "once"
				else f"Included based on {task.frequency} frequency"
			)
			for task in ordered_tasks
		}
		return self.today_plan

	def mark_task_complete(self, task_id: int) -> bool:  # Optional helper (not required for MVP)
		"""Mark a task complete by id and return True on success."""
		for task in self.retrieve_all_tasks():
			if task.task_id == task_id:
				task.mark_done()
				return True
		return False

	def explain_plan(self) -> str:
		"""Return a human-readable explanation of the current daily plan."""
		if not self.today_plan:
			return "No tasks scheduled for today."

		lines: list[str] = []
		for task in self.today_plan:
			reason = self.plan_reasons.get(task.task_id, "Included in today's plan")
			lines.append(f"- {task.description}: {reason}")
		return "\n".join(lines)
