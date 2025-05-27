from fastapi import APIRouter

from app.tasks.schemas import SchemaTask, SchemaTaskAdd, SchemaTaskUpdate
from app.tasks.service import TaskService

router = APIRouter(
    prefix="/task",
    tags=["Tasks"]
)

@router.get("")
async def get_all_task() -> list[SchemaTask]:
    return await TaskService.find_all()

@router.get("/{task_id}")
async def get_task_by_id(task_id:int) -> SchemaTask | None:
    return await TaskService.find_by_id(task_id)

@router.post("")
async def add_task(new_task: SchemaTaskAdd) -> SchemaTask:
    return await TaskService.add(
        name=new_task.name,
        description=new_task.description,
        project_id=new_task.project_id,
        creator_id=new_task.creator_id,
        assignee_id=new_task.assignee_id,
        priority=new_task.priority,
        due_date=new_task.due_date if new_task.due_date is not None else None,
        status=1,
        local_task_id=1
    )

@router.patch("")
async def update_task(data: SchemaTaskUpdate) -> SchemaTask:
    return await TaskService.update_by_id(
        data.id,
        name=data.name,
        description=data.description,
        project_id=data.project_id,
        assignee_id=data.assignee_id,
        priority=data.priority,
        due_date=data.due_date
    )

@router.delete("")
async def delete_task(id_task: int):
    return await TaskService.delete_by_id(id_task)