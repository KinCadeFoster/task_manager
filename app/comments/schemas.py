from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SchemaCommentAdd(BaseModel):
    """Схема для добавления комментария"""
    task_id: int = Field(..., description="Идентификатор задачи")
    comment_text: str = Field(..., description="Комментарий пользователя")

class SchemaComment(SchemaCommentAdd):
    """Схема комментария с дополнительными метаданными"""
    id: int = Field(..., description="Уникальный идентификатор комментария")
    creator_id: int = Field(..., description="Идентификатор создателя комментария")
    created_at: datetime = Field(..., description="Дата и время создания комментария")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления комментария")
    is_deleted: bool = Field(False, description="Удален ли комментарий")

    model_config = ConfigDict(from_attributes=True)

class SchemaCommentUpdate(BaseModel):
    """Схема для обновления текста комментария"""
    comment_text: str | None = Field(None, description="Комментарий пользователя")