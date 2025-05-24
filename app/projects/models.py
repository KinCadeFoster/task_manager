from sqlalchemy import String, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class ProjectTableModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="Уникальный идентификатор проекта")
    name: Mapped[str] = mapped_column(nullable=False, comment="Название проекта")
    prefix_name: Mapped[str] = mapped_column(String(5),nullable=False, unique=True, comment="Префикс проекта")
    description: Mapped[str] = mapped_column(nullable=False, comment="Описание проекта")
    creator_id: Mapped[int] = mapped_column(nullable=False, comment="ID создателя проекта")
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
        comment="Дата и время создания проекта"
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Дата и время последнего обновления проекта"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="Статус активности проекта")