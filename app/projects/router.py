from fastapi import APIRouter, Depends, status

from app.projects.schemas import SchemaProject, SchemaProjectAdd, SchemaProjectUpdate
from app.projects.service import ProjectService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel
from app.users.schemas import SchemaUser

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("/", response_model=list[SchemaProject])
async def get_all_projects(current_user: UsersTableModel = Depends(get_current_user)):
    return await ProjectService.get_all_project(current_user)

@router.get("/{project_id}", response_model=SchemaProject)
async def get_project_by_id(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await ProjectService.get_project_by_id(project_id, current_user)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SchemaProject)
async def add_project(
        new_project: SchemaProjectAdd,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await ProjectService.add_project(new_project, current_user)

@router.patch("/{project_id}", response_model=SchemaProject)
async def update_project(
        project_id: int,
        data: SchemaProjectUpdate,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await ProjectService.update_project(project_id, data, current_user)

@router.patch("/inactivate/{project_id}", response_model=SchemaProject)
async def inactivate_project(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await ProjectService.inactivate_project(project_id, current_user)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await ProjectService.delete_project(project_id, current_user)

@router.get("/{project_id}/users", response_model=list[SchemaUser])
async def get_project_users(
        project_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await ProjectService.get_project_users(project_id, current_user)

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
    return await ProjectService.remove_user_from_project(project_id, user_id, current_user)
