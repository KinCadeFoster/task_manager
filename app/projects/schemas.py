from datetime import datetime

from pydantic import BaseModel, Field, constr


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

    class Config:
        from_attributes = True