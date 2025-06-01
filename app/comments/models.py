from typing import Optional
from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class CommentTableModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, comment="Уникальный идентификатор комментария"
    )
    creator_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, comment="ID пользователя, создавшего комментарий"
    )
    comment_text: Mapped[str] = mapped_column(
        String(10000), nullable=False, comment="Текст комментария"
)
    task_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, comment="ID задачи, к которой относится комментарий"
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Флаг удаления"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        comment="Дата и время создания комментария"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="Дата и время последнего обновления комментария"
    )