from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SchemaUserRegister(BaseModel):
    email: EmailStr = Field(..., description="email пользователя")
    password: str = Field(..., description="Пароль пользователя")
    name: str = Field(..., description="Имя пользователя")
    surname: str = Field(..., description="Фамилия пользователя")
    patronymic: str = Field(..., description="Отчество пользователя")
    username: str = Field(..., description="Аккаунт пользователя")
    is_admin: bool = Field(description="Права админа")
    is_manager: bool = Field(description="Права менеджера")
    is_user: bool = Field(description="Пользователя")

class SchemaUser(BaseModel):
    id: int = Field(..., description="Идентификатор пользователя")
    email: EmailStr = Field(..., description="email пользователя")
    name: str = Field(..., description="Имя пользователя")
    surname: str = Field(..., description="Фамилия пользователя")
    patronymic: str = Field(..., description="Отчество пользователя")
    username: str = Field(..., description="Аккаунт пользователя")
    created_at: datetime = Field(..., description="Дата и время создания пользователя")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления данных пользователя")
    is_active: bool = Field(..., description="Удален ли пользователь")
    is_admin: bool = Field(description="Права админа")

    class Config:
        from_attributes = True

class SchemaUserAuth(BaseModel):
    username: str = Field(..., description="Аккаунт пользователя")
    password: str = Field(..., description="Пароль пользователя")