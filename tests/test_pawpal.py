from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task("Give medication", 5, "daily")

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 30, "daily")

    pet.add_task(task)

    assert len(pet.tasks) == 1
