from fastapi import APIRouter

from app.database import async_session_maker
from app.projects.models import ProjectTableModel
from app.projects.schemas import SchemaProject, SchemaProjectAdd

from app.projects.service import ProjectService

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("")
async def get_all_project() -> list[SchemaProject]:
    return await ProjectService.find_all()

@router.get("/{project_id}")
async def get_project_by_id(project_id:int) -> SchemaProject | None:
    return await ProjectService.find_by_id(project_id)


@router.post("")
async def add_project(new_project: SchemaProjectAdd):
    async with async_session_maker() as session:
        project = ProjectTableModel(
            name=new_project.name,
            description=new_project.description,
            creator_id=new_project.creator_id,
            prefix_name=new_project.prefix_name
        )
        session.add(project)
        await session.commit()
        return "staus: OK"