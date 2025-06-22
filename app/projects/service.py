from typing import Optional

from app.exceptions import UserPermissionError
from app.projects.exeptions import UserAlreadyInProject, CannotRemoveCreator, UserNotInProject
from app.projects.models import ProjectTableModel
from app.projects.schemas import SchemaProject
from app.tasks.exeptions import ProjectNotFound
from app.users.exeptions import UserNotFound
from app.users.models import UsersTableModel
from app.database import async_session_maker
from fastapi import HTTPException

from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.service.base import BaseService

class ProjectService(BaseService):
    model = ProjectTableModel

    @classmethod
    async def _find_by_id_inner(cls, project_id: int, session) -> Optional[ProjectTableModel]:
        result = await session.execute(
            select(ProjectTableModel)
            .options(selectinload(ProjectTableModel.users))
            .where(ProjectTableModel.id == project_id)
        )
        project = result.scalar_one_or_none()
        if not project:
            raise ProjectNotFound
        return project


    @classmethod
    async def find_by_id(cls, project_id: int, db_session=None) -> Optional[ProjectTableModel]:
        """
        Получить проект по id.
        Если db_session не передан — создаём и управляем собственной сессией.
        Если db_session передан — используем её (например, для модификации объекта).
        """
        should_open_session = False
        if db_session is None:
            db_session = async_session_maker()
            should_open_session = True

        if should_open_session:
            async with db_session as session:
                return await cls._find_by_id_inner(project_id, session)
        else:
            return await cls._find_by_id_inner(project_id, db_session)


    @classmethod
    async def add_user_to_project(cls, project_id: int, user_id: int, current_user: UsersTableModel):
        async with async_session_maker() as session:
            project = await cls.find_by_id(project_id, session)
            if not (current_user.is_manager and project.creator_id == current_user.id):
                raise UserPermissionError
            user = await session.get(UsersTableModel, user_id)
            if not user:
                raise UserNotFound
            if user in project.users:
                raise UserAlreadyInProject
            project.users.append(user)
            session.add(project)
            await session.commit()
            return {"detail": "User added to project"}


    @classmethod
    async def remove_user_from_project(cls, project_id: int, user_id: int, current_user: UsersTableModel):
        async with async_session_maker() as session:
            project = await cls.find_by_id(project_id, session)
            if not (current_user.is_manager and project.creator_id == current_user.id):
                raise UserPermissionError
            if user_id == project.creator_id:
                raise CannotRemoveCreator
            user = await session.get(UsersTableModel, user_id)
            if not user:
                raise UserNotFound
            if user not in project.users:
                raise UserNotInProject
            project.users.remove(user)
            session.add(project)
            await session.commit()
            return None


    @classmethod
    async def user_in_project(cls, project_id: int, user_id: int) -> bool:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        try:
            project = await cls.find_by_id(project_id)
        except HTTPException:
            return False
        return any(user.id == user_id for user in project.users)


    @classmethod
    async def find_by_user_id(cls, user_id: int) -> list[SchemaProject]:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            result = await session.execute(
                select(ProjectTableModel)
                .where(
                    or_(ProjectTableModel.creator_id == user_id,
                        ProjectTableModel.users.any(id=user_id))
                )
                .options(selectinload(ProjectTableModel.users))
                .order_by(ProjectTableModel.created_at.desc())
            )
            projects = result.scalars().all()
            return [SchemaProject.model_validate(project) for project in projects]