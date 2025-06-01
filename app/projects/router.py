from fastapi import APIRouter, Depends, HTTPException, status
from app.projects.schemas import SchemaProject, SchemaProjectAdd, SchemaProjectUpdate

from app.projects.service import ProjectService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("/")
async def get_all_project(user: UsersTableModel = Depends(get_current_user))-> list[SchemaProject]:
    return await ProjectService.find_all()

@router.get("/{project_id}")
async def get_project_by_id(project_id:int) -> SchemaProject:
    project = await ProjectService.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_project(new_project: SchemaProjectAdd) -> SchemaProject:
    return await ProjectService.add(**new_project.model_dump())

@router.patch("/{project_id}")
async def update_project(project_id: int, data: SchemaProjectUpdate) -> SchemaProject:
    project = await ProjectService.update_by_id(project_id, **data.model_dump())
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int):
    result = await ProjectService.delete_by_id(project_id)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return None