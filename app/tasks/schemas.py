from datetime import datetime
from pydantic import BaseModel, Field

class SchemaTaskAdd(BaseModel):
    name: str = Field(..., description="Название задачи", examples=["Баг отображения"])
    description: str | None = Field(None, description="Описание задачи")
    project_id: int = Field(..., description="ID проекта")
    assignee_id: int = Field(..., description="ID исполнителя")
    priority: int = Field(..., description="Приоритет", examples=[1])
    due_date: datetime | None = Field(None, description="Дедлайн")

class SchemaTask(SchemaTaskAdd):
    id: int = Field(..., description="ID задачи")
    creator_id: int = Field(..., description="ID создателя задачи")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")
    status: int = Field(..., description="Статус", examples=[1])
    local_task_id: int = Field(..., description="Локальный номер задачи", examples=[1])

    class Config:
        from_attributes = True

class SchemaTaskUpdate(BaseModel):
    name: str = Field(..., description="Название задачи", examples=["Баг отображения"])
    description: str | None = Field(None, description="Описание задачи")
    project_id: int = Field(..., description="ID проекта")
    assignee_id: int = Field(..., description="ID исполнителя")
    priority: int = Field(..., description="Приоритет", examples=[1])
    due_date: datetime | None = Field(None, description="Дедлайн")