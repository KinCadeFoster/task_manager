from fastapi import APIRouter, Depends, status

from app.exceptions import UserPermissionError
from app.projects.exeptions import NewCreatorNotFound, NewCreatorMustBeManager, ProjectAlreadyInactive, \
    ProjectMustBeInactive
from app.projects.schemas import SchemaProject, SchemaProjectAdd, SchemaProjectUpdate

from app.projects.service import ProjectService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel
from app.users.schemas import SchemaUser
from app.users.service import UsersService

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("/")
async def get_all_project(
        current_user: UsersTableModel = Depends(get_current_user)
)-> list[SchemaProject]:
    if current_user.is_admin:
        return await ProjectService.find_all()
    return await ProjectService.find_by_user_id(current_user.id)


@router.get("/{project_id}")
async def get_project_by_id(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaProject:
    project = await ProjectService.find_by_id(project_id)
    if current_user.is_admin or project.creator_id == current_user.id or any(u.id == current_user.id for u in project.users):
        return SchemaProject.model_validate(project)
    raise UserPermissionError


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_project(
        new_project: SchemaProjectAdd,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaProject:
    if current_user.is_manager:
        current_project = await ProjectService.add(**new_project.model_dump(), creator_id=current_user.id)
        await add_user_to_project(current_project.id, current_user.id)
        return current_project
    raise UserPermissionError


@router.patch("/{project_id}")
async def update_project(
        project_id: int,
        data: SchemaProjectUpdate,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaProject:
    project = await ProjectService.find_by_id(project_id)
    if current_user.is_manager and project.creator_id == current_user.id:
        if project.creator_id != data.creator_id:
            new_creator = await UsersService.find_by_id(data.creator_id)
            if not new_creator:
                raise NewCreatorNotFound
            if not new_creator.is_manager:
                raise NewCreatorMustBeManager
            await add_user_to_project(project.id, data.creator_id)
        return await ProjectService.update_by_id(project_id, **data.model_dump())
    raise UserPermissionError


@router.patch("/inactivate/{project_id}")
async def inactivate_project(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaProject:
    project = await ProjectService.find_by_id(project_id)
    if not (current_user.is_manager and project.creator_id == current_user.id):
        raise UserPermissionError
    if not project.is_active:
        raise ProjectAlreadyInactive
    return await ProjectService.update_by_id(project_id, is_active=False)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    project = await ProjectService.find_by_id(project_id)
    if not current_user.is_admin:
        raise UserPermissionError
    if project.is_active:
        raise ProjectMustBeInactive
    await ProjectService.delete_by_id(project_id)
    return None


@router.get("/{project_id}/users")
async def get_project_users(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
) -> list[SchemaUser]:
    project = await ProjectService.find_by_id(project_id)
    if not any(u.id == current_user.id for u in project.users):
        raise UserPermissionError
    return [SchemaUser.model_validate(user) for user in project.users]


@router.post("/{project_id}/users/{user_id}", status_code=status.HTTP_200_OK)
async def add_user_to_project(
        project_id: int,
        user_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await ProjectService.add_user_to_project(project_id, user_id, current_user)


@router.delete("/{project_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_from_project(
        project_id: int,
        user_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    await ProjectService.remove_user_from_project(project_id, user_id, current_user)
    return None
