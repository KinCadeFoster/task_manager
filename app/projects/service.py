from typing import Optional, Any

from app.projects.models import ProjectTableModel
from app.projects.schemas import SchemaProject
from app.users.models import UsersTableModel
from app.database import async_session_maker
from fastapi import HTTPException

from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload

from app.service.base import BaseService

class ProjectService(BaseService):
    model = ProjectTableModel

    @classmethod
    async def add_user_to_project(cls, project_id: int, user_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(ProjectTableModel)
                .options(selectinload(ProjectTableModel.users))
                .where(ProjectTableModel.id == project_id)
            )
            project = result.scalar_one_or_none()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            user = await session.get(UsersTableModel, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if user in project.users:
                raise HTTPException(status_code=400, detail="User already in project")
            project.users.append(user)
            session.add(project)
            await session.commit()

    @classmethod
    async def remove_user_from_project(cls, project_id: int, user_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(ProjectTableModel)
                .options(selectinload(ProjectTableModel.users))
                .where(ProjectTableModel.id == project_id)
            )
            project = result.scalar_one_or_none()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            user = await session.get(UsersTableModel, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if user not in project.users:
                raise HTTPException(status_code=400, detail="User not in project")
            project.users.remove(user)
            session.add(project)
            await session.commit()

    @classmethod
    async def find_users_in_project(cls, model_id: int, options=None) -> Optional[Any]:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            if options:
                for opt in options:
                    query = query.options(opt)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def user_in_project(cls, project_id: int, user_id: int) -> bool:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            result = await session.execute(
                select(ProjectTableModel)
                .options(selectinload(ProjectTableModel.users))
                .where(ProjectTableModel.id == project_id)
            )
            project = result.scalar_one_or_none()
            if not project:
                return False
            return any(user.id == user_id for user in project.users)

    @classmethod
    async def find_by_user_id(cls, user_id: int) -> list[SchemaProject]:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            query = (
                select(ProjectTableModel)
                .where(
                    or_(ProjectTableModel.creator_id == user_id,
                        ProjectTableModel.users.any(id=user_id))
                )
                .options(joinedload(ProjectTableModel.users))
                .order_by(ProjectTableModel.created_at.desc())
            )
            result = await session.execute(query)
            projects = result.unique().scalars().all()

            return [SchemaProject.model_validate(project) for project in projects]

    @classmethod
    async def find_by_id(cls, project_id: int) -> Optional[ProjectTableModel]:
        async with async_session_maker() as session:
            query = (
                select(ProjectTableModel)
                .where(ProjectTableModel.id == project_id)
                .options(joinedload(ProjectTableModel.users))
            )
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()