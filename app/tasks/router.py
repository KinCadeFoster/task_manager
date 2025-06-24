from fastapi import APIRouter, status, Depends

from app.tasks.schemas import SchemaTask, SchemaTaskAdd, SchemaTaskUpdate
from app.tasks.service import TaskService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel

router = APIRouter(prefix="/tasks",tags=["Tasks"])


@router.get("/{task_id}", response_model=SchemaTask)
async def get_task_by_id(task_id:int, current_user: UsersTableModel = Depends(get_current_user)):
    return await TaskService.get_task_by_id(task_id, current_user)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SchemaTask)
async def add_task(new_task: SchemaTaskAdd, current_user: UsersTableModel = Depends(get_current_user)):
    return await TaskService.add_task(new_task, current_user)

@router.patch("/{task_id}", response_model=SchemaTask)
async def update_task(task_id: int, data: SchemaTaskUpdate, current_user: UsersTableModel = Depends(get_current_user)):
    return await TaskService.update_task(task_id, data, current_user)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, current_user: UsersTableModel = Depends(get_current_user)):
    return await TaskService.delete_task(task_id, current_user)

@router.get("/tasks-by-project/{project_id}", response_model=list[SchemaTask])
async def get_tasks_by_project(project_id: int, current_user: UsersTableModel = Depends(get_current_user)):
    return await TaskService.get_tasks_by_project(project_id, current_user)

@router.get("/{project_prefix}-{local_task_id}", response_model=SchemaTask)
async def get_tasks_by_project(
        project_prefix: str,
        local_task_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await TaskService.get_tasks_by_prefix_and_id(project_prefix, local_task_id, current_user)