from sqlalchemy import select

from app.database import async_session_maker
from app.service.base import BaseService
from app.tasks.models import TaskTableModel


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