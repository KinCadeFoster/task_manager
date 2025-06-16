from sqlalchemy import select

from app.database import async_session_maker
from app.projects.service import ProjectService
from app.service.base import BaseService
from app.tasks.dependencies import check_access_for_tasks
from app.tasks.exeptions import TaskNotFound, ProjectNotFound
from app.tasks.models import TaskTableModel
from app.tasks.schemas import SchemaTaskAdd, SchemaTaskUpdate
from app.users.models import UsersTableModel


class TaskService(BaseService):
    model = TaskTableModel

    @classmethod
    async def get_project_id_by_task_id(cls, task_id: int, options=None) -> int:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            query = select(cls.model.project_id).where(cls.model.id == task_id)
            result = await session.execute(query)
            project_id = result.scalar_one_or_none()
            if project_id is None:
                from fastapi import HTTPException
                raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
            return project_id

    @classmethod
    async def get_task_by_id(cls, task_id:int, current_user: UsersTableModel):
        await check_access_for_tasks(task_id, current_user)
        task = await TaskService.find_by_id(task_id)
        if not task:
            raise TaskNotFound
        return task

    @classmethod
    async def add_task(cls, new_task: SchemaTaskAdd, current_user: UsersTableModel):
        await check_access_for_tasks(new_task.project_id, current_user)
        project = await ProjectService.find_by_id(new_task.project_id)
        if not project:
            raise ProjectNotFound
        new_task_dict = new_task.model_dump()
        return await TaskService.add(**new_task_dict, creator_id=current_user.id, status=1, local_task_id=1)

    @classmethod
    async def update_task(cls, task_id: int, data: SchemaTaskUpdate, current_user: UsersTableModel):
        await check_access_for_tasks(task_id, current_user)
        task = await TaskService.update_by_id(task_id, **data.model_dump())
        if not task:
            raise TaskNotFound
        return task

    @classmethod
    async def delete_task(cls, task_id: int, current_user: UsersTableModel):
        await check_access_for_tasks(task_id, current_user)
        task = await TaskService.find_by_id(task_id)
        if not task:
            raise TaskNotFound
        result = await TaskService.delete_by_id(task_id)
        if not result:
            raise TaskNotFound
        return None

    @classmethod
    async def get_tasks_by_project(cls, project_id: int, current_user: UsersTableModel):
        await check_access_for_tasks(project_id, current_user)
        project = await ProjectService.find_by_id(project_id)
        if not project:
            raise ProjectNotFound
        return await TaskService.find_all(project_id=project_id)