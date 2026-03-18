from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
	task_id: int
	title: str
	duration_minutes: int
	priority: int
	status: str

	def mark_done(self) -> None:
		pass


@dataclass
class Pet:
	pet_id: int
	name: str
	species: str
	owner_id: int
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def get_tasks_for_date(self, target_date: date) -> list[Task]:
		pass


class Owner:
	def __init__(self, owner_id: int, name: str, available_minutes_per_day: int) -> None:
		self.owner_id = owner_id
		self.name = name
		self.available_minutes_per_day = available_minutes_per_day
		self.pets: list[Pet] = []

	def add_pet(self, pet: Pet) -> None:
		pass

	def get_all_tasks(self) -> list[Task]:
		pass


class Scheduler:
	def __init__(self, owner: Owner) -> None:
		self.owner = owner
		self.today_plan: list[Task] = []

	def generate_daily_plan(self, target_date: date) -> list[Task]:
		pass

	def explain_plan(self) -> str:
		pass
