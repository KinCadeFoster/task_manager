from datetime import datetime

from pydantic import BaseModel, Field


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

    class Config:
        from_attributes = True