from typing import Optional

from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TaskTableModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="Уникальный идентификатор задачи")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Название задачи")
    description: Mapped[str | None] = mapped_column(String(10000), nullable=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    creator_id: Mapped[int] = mapped_column(Integer, nullable=False)
    assignee_id: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, comment="Приоритет задачи")

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        comment="Дата и время создания задачи"
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default= func.now(),
        onupdate= func.now(),
        comment="Дата и время последнего обновления задачи"
    )

    status: Mapped[int] = mapped_column(Integer, nullable=False,comment="Статус задачи")
    due_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата и время завершения задачи"
    )

    local_task_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="Номер задачи в проекте")