from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SchemaUserRegister(BaseModel):
    email: EmailStr = Field(..., description="email пользователя")
    password: str = Field(..., description="Пароль пользователя")
    name: str = Field(..., description="Имя пользователя")
    surname: str = Field(..., description="Фамилия пользователя")
    patronymic: str = Field(..., description="Отчество пользователя") # None по умолчанию, если не обязательно
    username: str = Field(..., description="Аккаунт пользователя")
    is_admin: bool = Field(default=False, description="Права админа")
    is_manager: bool = Field(default=False, description="Права менеджера")
    is_user: bool = Field(default=True, description="Пользователь")


class SchemaUser(BaseModel):
    id: int = Field(..., description="Идентификатор пользователя")
    email: EmailStr = Field(..., description="email пользователя")
    name: str = Field(..., description="Имя пользователя")
    surname: str = Field(..., description="Фамилия пользователя")
    patronymic: str = Field(..., description="Отчество пользователя")
    username: str = Field(..., description="Аккаунт пользователя")
    created_at: datetime = Field(..., description="Дата и время создания пользователя")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления данных пользователя")
    is_active: bool = Field(..., description="Активен ли пользователь")
    is_admin: bool = Field(default=False, description="Права админа")
    is_manager: bool = Field(default=False, description="Права менеджера")
    is_user: bool = Field(default=True, description="Пользователь")

    class Config:
        from_attributes = True

class SchemaUserAuth(BaseModel):
    username: str = Field(..., description="Аккаунт пользователя")
    password: str = Field(..., description="Пароль пользователя")