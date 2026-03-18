from pawpal_system import Pet, Task


def test_task_completion_marks_task_done() -> None:
	task = Task(task_id=1, pet_id=101, description="Morning walk")

	task.mark_done()

	assert task.is_completed is True


def test_add_task_increases_pet_task_count() -> None:
	pet = Pet(pet_id=101, name="Milo", species="Dog", owner_id=1)
	initial_count = len(pet.tasks)
	task = Task(task_id=2, pet_id=101, description="Feed breakfast")

	pet.add_task(task)

	assert len(pet.tasks) == initial_count + 1
