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
    return "staus: OK"