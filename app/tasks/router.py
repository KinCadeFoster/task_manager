from fastapi import APIRouter, HTTPException, status, Depends

from app.comments.dependencies import check_access_for_comments
from app.projects.service import ProjectService
from app.tasks.dependencies import check_user_can_access_task_for_manager_or_user_tasks
from app.tasks.schemas import SchemaTask, SchemaTaskAdd, SchemaTaskUpdate
from app.tasks.service import TaskService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel

router = APIRouter(prefix="/tasks",tags=["Tasks"])

@router.get("/")
async def get_all_tasks() -> list[SchemaTask]:
    return await TaskService.find_all()

@router.get("/{task_id}", response_model=SchemaTask)
async def get_task_by_id(task_id:int, current_user: UsersTableModel = Depends(get_current_user)):
    await check_access_for_comments(task_id, current_user)
    task = await TaskService.find_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SchemaTask)
async def add_task(new_task: SchemaTaskAdd, current_user: UsersTableModel = Depends(get_current_user)):
    await check_user_can_access_task_for_manager_or_user_tasks(new_task.project_id, current_user)
    project = await ProjectService.find_by_id(new_task.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    new_task_dict = new_task.model_dump()
    new_task_dict["creator_id"] = current_user.id
    new_task_dict["status"] = 1
    new_task_dict["local_task_id"] = 1
    return await TaskService.add(**new_task_dict)

@router.patch("/{task_id}", response_model=SchemaTask)
async def update_task(task_id: int, data: SchemaTaskUpdate, current_user: UsersTableModel = Depends(get_current_user)):
    await check_access_for_comments(task_id, current_user)
    task = await TaskService.update_by_id(task_id, **data.model_dump())
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, current_user: UsersTableModel = Depends(get_current_user)):
    await check_access_for_comments(task_id, current_user)
    task = await TaskService.find_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    result = await TaskService.delete_by_id(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@router.get("/tasks-by-project/{project_id}", response_model=list[SchemaTask])
async def get_tasks_by_project(project_id: int, current_user: UsersTableModel = Depends(get_current_user)):
    await check_user_can_access_task_for_manager_or_user_tasks(project_id, current_user)
    project = await ProjectService.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return await TaskService.find_all(project_id=project_id)