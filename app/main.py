from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field, constr

from app.projects.router import router as router_projects
from app.tasks.router import router as router_tasks

app = FastAPI()

app.include_router(router_tasks)
app.include_router(router_projects)










class SchemaCommentAdd(BaseModel):
    project_id: int
    task_id: int
    description: str
    autor_id: int


class SchemaComment(SchemaCommentAdd):
    id: int
    created_at: datetime = Field(..., description="Дата создания", examples=["2025-05-08T17:19:33.900197"])
    updated_at: datetime = Field(..., description="Дата последнего обновления", examples=["2025-05-08T17:19:33.900200"])


@app.get("/comment")
async def get_all_comment() -> list[SchemaComment]:
    return "staus: OK"

@app.post("/comment")
async def add_comment(new_comment: SchemaCommentAdd):
    return "staus: OK"