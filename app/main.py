from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field, constr

app = FastAPI()


class SchemaTaskAdd(BaseModel):
    name: str = Field(..., description="Название задачи", examples=["Баг отображения"])
    description: str | None = Field(None, description="Описание задачи")
    project_id: int = Field(..., description="Идентификатор проекта, к которому относится задача")
    creator_id: int = Field(..., description="Идентификатор создателя задачи")
    assignee_id: int = Field(..., description="Идентификатор пользователя, назначенного на задачу")
    priority: int = Field(..., description="Приоритет задачи",examples=[1])
    due_date: datetime | None = Field(None, description="Дата и время завершения задачи")

class SchemaTask(SchemaTaskAdd):
    id: int = Field(..., description="Уникальный идентификатор задачи")
    created_at: datetime = Field(..., description="Дата и время создания задачи")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления задачи")
    status: int = Field(..., description="Текущий статус задачи", examples=[1])
    local_task_id: int = Field(..., description="Номер задачи в проекте", examples=[1])



@app.get("/task")
async def get_all_task() -> list[SchemaTask]:
    return "staus: OK"

@app.get("/task/{task_id}")
async def get_task_by_id(task_id:int) -> SchemaTask:
    return task_id

@app.post("/task")
async def add_task(new_task: SchemaTaskAdd):
    return "staus: OK"


class SchemaProjectAdd(BaseModel):
    name: str = Field(..., description="Название проекта", examples=["My Project"])
    prefix_name: constr(min_length=3, max_length=5, pattern=r"^[A-Z]{3,5}$") = Field(...,
                        description="Префикс проекта (уникальный короткий код)", examples=["MPP"])
    description: str = Field(..., description="Описание проекта", examples=["Проект для автоматизации задач"])
    creator_id: int = Field(..., description="ID пользователя, создавшего проект", examples=[1])


class SchemaProject(SchemaProjectAdd):
    id: int = Field(..., description="Уникальный ID проекта", examples=[101])
    created_at: datetime = Field(..., description="Дата создания", examples=["2025-05-08T17:19:33.900197"])
    updated_at: datetime = Field(..., description="Дата последнего обновления", examples=["2025-05-08T17:19:33.900200"])
    is_active: bool = Field(..., description="Флаг активности проекта", examples=[True])


@app.get("/project")
async def get_all_project() -> list[SchemaProject]:
    return "staus: OK"

@app.get("/project/{project_id}")
async def get_project_by_id(project_id:int) -> SchemaProject:
    return "staus: OK"


@app.post("/project")
async def add_project(new_project: SchemaProjectAdd):
    return "staus: OK"

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