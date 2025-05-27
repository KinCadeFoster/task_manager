from fastapi import APIRouter, Depends
from watchfiles import awatch

from app.database import async_session_maker
from app.projects.models import ProjectTableModel
from app.projects.schemas import SchemaProject, SchemaProjectAdd, SchemaProjectUpdate

from app.projects.service import ProjectService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("")
async def get_all_project(user: UsersTableModel = Depends(get_current_user))-> list[SchemaProject]:
    return await ProjectService.find_all()

@router.get("/{project_id}")
async def get_project_by_id(project_id:int) -> SchemaProject | None:
    return await ProjectService.find_by_id(project_id)


@router.post("")
async def add_project(new_project: SchemaProjectAdd) -> SchemaProject:
    return await ProjectService.add(
        name=new_project.name,
        prefix_name=new_project.prefix_name,
        description=new_project.description,
        creator_id=new_project.creator_id
    )

@router.patch("")
async def update_project(data: SchemaProjectUpdate) -> SchemaProject:
    return await ProjectService.update_by_id(data.id, name=data.name, description=data.description)

@router.delete("")
async def delete_project(id_project: int):
    return await ProjectService.delete_by_id(id_project)