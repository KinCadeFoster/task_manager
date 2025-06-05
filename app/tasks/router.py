from fastapi import APIRouter, HTTPException,status

from app.projects.service import ProjectService
from app.tasks.schemas import SchemaTask, SchemaTaskAdd, SchemaTaskUpdate
from app.tasks.service import TaskService

router = APIRouter(prefix="/tasks",tags=["Tasks"])

@router.get("/")
async def get_all_task() -> list[SchemaTask]:
    return await TaskService.find_all()

@router.get("/{task_id}")
async def get_task_by_id(task_id:int) -> SchemaTask:
    task = await TaskService.find_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/")
async def add_task(new_task: SchemaTaskAdd) -> SchemaTask:
    project = await ProjectService.find_by_id(new_task.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return await TaskService.add(**new_task.model_dump(), status=1, local_task_id=1)

@router.patch("/{task_id}")
async def update_task(task_id: int, data: SchemaTaskUpdate) -> SchemaTask:
    task = await TaskService.update_by_id(task_id, **data.model_dump())
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    result = await TaskService.delete_by_id(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@router.get("/by-project/{project_id}")
async def get_tasks_by_project(project_id: int) -> list[SchemaTask]:
    project = await ProjectService.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return await TaskService.find_all(project_id=project_id)