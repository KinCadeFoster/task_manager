from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload

from app.exceptions import UserPermissionError
from app.projects.models import ProjectTableModel
from app.projects.schemas import SchemaProject, SchemaProjectAdd, SchemaProjectUpdate

from app.projects.service import ProjectService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel
from app.users.schemas import SchemaUser

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
    else:
        return await ProjectService.find_by_user_id(current_user.id)

@router.get("/{project_id}")
async def get_project_by_id(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaProject:
    project = await ProjectService.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.is_admin or project.creator_id == current_user.id or any(u.id == current_user.id for u in project.users):
        return SchemaProject.model_validate(project)
    raise UserPermissionError

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_project(
        new_project: SchemaProjectAdd,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaProject:
    if current_user.is_manager:
        return await ProjectService.add(**new_project.model_dump(), creator_id=current_user.id)
    raise UserPermissionError


@router.patch("/{project_id}")
async def update_project(
        project_id: int,
        data: SchemaProjectUpdate,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaProject:
    project = await ProjectService.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.is_manager and project.creator_id == current_user.id:
        return await ProjectService.update_by_id(project_id, **data.model_dump())
    raise UserPermissionError

@router.patch("/inactivate/{project_id}")
async def inactivate_project(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaProject:
    project = await ProjectService.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not (current_user.is_manager and project.creator_id == current_user.id):
        raise UserPermissionError
    if not project.is_active:
        raise HTTPException(status_code=409, detail="Project already inactive")
    return await ProjectService.update_by_id(project_id, is_active=False)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    project = await ProjectService.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not current_user.is_admin:
        raise UserPermissionError
    if project.is_active:
        raise HTTPException(status_code=400, detail="Project must be inactive before deletion")
    await ProjectService.delete_by_id(project_id)

@router.get("/{project_id}/users")
async def get_project_users(project_id: int) -> list[SchemaUser]:
    project = await ProjectService.find_users_in_project(project_id, options=[selectinload(ProjectTableModel.users)])
    return [SchemaUser.model_validate(user) for user in project.users]

@router.post("/{project_id}/users/{user_id}", status_code=status.HTTP_200_OK)
async def add_user_to_project(project_id: int, user_id: int):
    await ProjectService.add_user_to_project(project_id, user_id)
    return {"detail": "User added to project"}

@router.delete("/{project_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_from_project(project_id: int, user_id: int):
    await ProjectService.remove_user_from_project(project_id, user_id)
    return None
