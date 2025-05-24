from fastapi import APIRouter

from app.tasks.schemas import SchemaTask, SchemaTaskAdd
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
async def add_task(new_task: SchemaTaskAdd):
    await TaskService.add(
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