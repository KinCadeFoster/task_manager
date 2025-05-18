from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field, constr

app = FastAPI()


@app.get("/task")
async def get_all_task():
    return "staus: OK"

@app.get("/task/{task_id}")
async def get_task_by_id(task_id:int):
    return task_id



class SchemaTaskAdd(BaseModel):
    name: str = Field(..., description="Название задачи", examples=["Баг отображения"])
    description: str | None = Field(None, description="Описание задачи")
    project_id: int = Field(..., description="Идентификатор проекта, к которому относится задача")
    creator_id: int = Field(..., description="Идентификатор создателя задачи")
    assignee_id: int = Field(..., description="Идентификатор пользователя, назначенного на задачу")
    priority: int = Field(..., description="Приоритет задачи",examples=[1])
    due_date: datetime | None = Field(None, description="Дата и время завершения задачи")


@app.post("task")
async def create_task(new_task: SchemaTaskAdd):
    return "staus: OK"

@app.get("/project")
async def get_all_project():
    return "staus: OK"

@app.get("/project/{project_id}")
async def get_project_by_id(project_id:int):
    return "staus: OK"


class SchemaProjectAdd(BaseModel):
    name: str = Field(..., description="Название проекта", examples=["My Project"])
    prefix_name: constr(min_length=3, max_length=5, pattern=r"^[A-Z]{3,5}$") = Field(...,
                        description="Префикс проекта (уникальный короткий код)", examples=["MPP"])
    description: str = Field(..., description="Описание проекта", examples=["Проект для автоматизации задач"])
    creator_id: int = Field(..., description="ID пользователя, создавшего проект", examples=[1])



@app.post("project")
async def create_project(new_project: SchemaProjectAdd):
    return "staus: OK"