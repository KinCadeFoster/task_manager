from typing import Optional

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CommentTableModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="Уникальный идентификатор комментария")
    creator_id: Mapped[int] = mapped_column(nullable=False)
    comment_text: Mapped[str] = mapped_column(String(10000), nullable=False)
    task_id: Mapped[int] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        comment="Дата и время создания комментария"
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default= func.now(),
        onupdate= func.now(),
        comment="Дата и время последнего обновления комментария"
    )