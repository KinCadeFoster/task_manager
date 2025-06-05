from sqlalchemy import String, DateTime, func, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.projects.association_tables import project_users

class ProjectTableModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="Уникальный идентификатор проекта")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Название проекта")
    prefix_name: Mapped[str] = mapped_column(String(5), nullable=False, unique=True, comment="Префикс проекта")
    description: Mapped[str] = mapped_column(String(1000), nullable=False, comment="Описание проекта")
    creator_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="ID создателя проекта")
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

    users = relationship("UsersTableModel", secondary=project_users, back_populates="projects")
    tasks = relationship("TaskTableModel", back_populates="project", cascade="all, delete-orphan")