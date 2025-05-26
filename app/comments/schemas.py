from datetime import datetime
from pydantic import BaseModel, Field


class SchemaCommentAdd(BaseModel):
    task_id: int = Field(..., description="Идентификатор задачи")
    creator_id: int = Field(..., description="Идентификатор создателя комментария")
    comment_text: str = Field(..., description="Комментарий пользователя")

class SchemaComment(SchemaCommentAdd):
    id: int = Field(..., description="Уникальный идентификатор комментария")
    created_at: datetime = Field(..., description="Дата и время создания комментария")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления комментария")
    is_deleted: bool = Field(..., description="Удален ли комментарий")

    class Config:
        from_attributes = True

class SchemaCommentUpdate(BaseModel):
    id: int = Field(..., description="Идентификатор комментария")
    comment_text: str = Field(..., description="Комментарий пользователя")
