from typing import Optional

from app.exceptions import UserPermissionError
from app.projects.exeptions import (
    UserAlreadyInProject, CannotRemoveCreator, UserNotInProject, NewCreatorNotFound,
    NewCreatorMustBeManager, ProjectAlreadyInactive, ProjectMustBeInactive
)
from app.projects.models import ProjectTableModel
from app.projects.schemas import SchemaProject, SchemaProjectAdd, SchemaProjectUpdate
from app.tasks.exeptions import ProjectNotFound
from app.users.exeptions import UserNotFound
from app.users.models import UsersTableModel
from app.database import async_session_maker

from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.service.base import BaseService
from app.users.schemas import SchemaUser
from app.users.service import UsersService

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
    async def find_by_id(cls, project_id: int, db_session=None) -> ProjectTableModel:
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
            if any(u.id == user.id for u in project.users):
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
            if not any(u.id == user.id for u in project.users):
                raise UserNotInProject
            project.users.remove(next(u for u in project.users if u.id == user.id))
            session.add(project)
            await session.commit()
            return None

    @classmethod
    async def user_in_project(cls, project_id: int, user_id: int) -> bool:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        try:
            project = await cls.find_by_id(project_id)
        except ProjectNotFound:
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

    @classmethod
    async def get_all_project(cls, current_user: UsersTableModel):
        if current_user.is_admin:
            return await ProjectService.find_all()
        return await cls.find_by_user_id(current_user.id)

    @classmethod
    async def get_project_by_id(cls, project_id: int, current_user: UsersTableModel):
        project = await cls.find_by_id(project_id)
        if (
            current_user.is_admin
            or project.creator_id == current_user.id
            or any(u.id == current_user.id for u in project.users)
        ):
            return SchemaProject.model_validate(project)
        raise UserPermissionError

    @classmethod
    async def add_project(cls, new_project: SchemaProjectAdd, current_user: UsersTableModel):
        if current_user.is_manager:
            current_project = await ProjectService.add(**new_project.model_dump(), creator_id=current_user.id)
            await cls.add_user_to_project(current_project.id, current_user.id, current_user)
            return current_project
        raise UserPermissionError

    @classmethod
    async def update_project(
            cls,
            project_id: int,
            data: SchemaProjectUpdate,
            current_user: UsersTableModel
    ):
        project = await cls.find_by_id(project_id)
        if current_user.is_manager and project.creator_id == current_user.id:
            if project.creator_id != data.creator_id:
                new_creator = await UsersService.find_by_id(data.creator_id)
                if not new_creator:
                    raise NewCreatorNotFound
                if not new_creator.is_manager:
                    raise NewCreatorMustBeManager
                if not any(u.id == new_creator.id for u in project.users):
                    await cls.add_user_to_project(project_id, data.creator_id, current_user)
            return await ProjectService.update_by_id(project_id, **data.model_dump())
        raise UserPermissionError

    @classmethod
    async def inactivate_project(cls, project_id: int, current_user: UsersTableModel):
        project = await cls.find_by_id(project_id)
        if not (current_user.is_manager and project.creator_id == current_user.id):
            raise UserPermissionError
        if not project.is_active:
            raise ProjectAlreadyInactive
        return await ProjectService.update_by_id(project_id, is_active=False)

    @classmethod
    async def delete_project(cls, project_id: int, current_user: UsersTableModel):
        project = await cls.find_by_id(project_id)
        if not current_user.is_admin:
            raise UserPermissionError
        if project.is_active:
            raise ProjectMustBeInactive
        await ProjectService.delete_by_id(project_id)
        return None

    @classmethod
    async def get_project_users(cls, project_id: int, current_user: UsersTableModel):
        project = await cls.find_by_id(project_id)
        if not (
            current_user.is_admin
            or project.creator_id == current_user.id
            or any(u.id == current_user.id for u in project.users)
        ):
            raise UserPermissionError
        return [SchemaUser.model_validate(user) for user in project.users]