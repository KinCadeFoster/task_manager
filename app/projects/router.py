from fastapi import APIRouter, Depends

from app.database import async_session_maker
from app.projects.models import ProjectTableModel
from app.projects.schemas import SchemaProject, SchemaProjectAdd

from app.projects.service import ProjectService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("")
async def get_all_project(user: UsersTableModel = Depends(get_current_user)): #-> list[SchemaProject]:
    return await ProjectService.find_all(creator_id=user.id)

@router.get("/{project_id}")
async def get_project_by_id(project_id:int) -> SchemaProject | None:
    return await ProjectService.find_by_id(project_id)


@router.post("")
async def add_project(new_project: SchemaProjectAdd):
    await ProjectService.add(
        name=new_project.name,
        prefix_name=new_project.prefix_name,
        description=new_project.description,
        creator_id=new_project.creator_id
    )