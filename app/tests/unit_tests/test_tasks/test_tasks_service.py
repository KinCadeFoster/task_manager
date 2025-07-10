import pytest

from app.tasks.service import TaskService


@pytest.mark.parametrize("name, description, project_id, assignee_id, priority, creator_id, status, local_task_id",[
    ("Task 1", None, 2, 2, 1, 2, 1, 5),
    ("Task 2", "Description task", 2, 2, 1, 2, 2, 6),
])

async def test_add_task_and_delete(name, description, project_id, assignee_id, priority, creator_id, status, local_task_id):
    task = await TaskService.add(name=name, description=description, project_id=project_id, assignee_id=assignee_id,
                                    priority=priority, creator_id=creator_id, status=status, local_task_id=local_task_id)

    assert task.name == name
    assert task.description == description
    assert task.project_id == project_id
    assert task.assignee_id == assignee_id
    assert task.priority == priority
    assert task.creator_id == creator_id
    assert task.status == status
    assert task.local_task_id == local_task_id

    await TaskService.delete_by_id(task.id)


async def test_find_task_by_id():
    task = await TaskService.find_by_id(1)

    assert task is not None


async def test_find_no_exist_task_by_id():
    task = await TaskService.find_by_id(999999)

    assert task is None


async def test_find_all_task():
    task = await TaskService.find_all(project_id=1)

    assert len(task) == 2

async def test_find_all_task_empty_list():
    task = await TaskService.find_all(project_id=9999)

    assert task == []


async def test_find_one_task_or_none():
    task = await TaskService.find_one_or_none(project_id=2)

    assert task is not None

async def test_find_one_task_or_none_no_exist():
    task = await TaskService.find_one_or_none(project_id=99999)

    assert task is None


@pytest.mark.parametrize("task_id, name, description, project_id, assignee_id, priority",[
    (1,"Task updated name 1", "Updated description", 1, 3, 2),
])

async def test_update_task(task_id, name, description, project_id, assignee_id, priority):
    updated_task = await TaskService.update_by_id(object_id=task_id, name=name, description=description,
                                                 project_id=project_id, assignee_id=assignee_id, priority=priority)

    assert updated_task.name == name
    assert updated_task.description == description
    assert updated_task.project_id == project_id
    assert updated_task.assignee_id == assignee_id
    assert updated_task.priority == priority


async def test_delete_task():
    task = await TaskService.delete_by_id(1)

    assert task == True


async def test_delete_task_not_exist():
    task = await TaskService.delete_by_id(999999)

    assert task == False
