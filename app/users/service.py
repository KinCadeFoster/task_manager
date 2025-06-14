from app.exceptions import UserAlreadyExistsException
from app.service.base import BaseService
from app.users.models import UsersTableModel


class UsersService(BaseService):
    model = UsersTableModel

    @classmethod
    async def check_unique_fields_on_update(cls, user_id: int, email: str = None, username: str = None):
        """Проверяет уникальность email и username для других пользователей"""
        if email:
            existing_user = await cls.find_one_or_none(email=email)
            if existing_user and existing_user.id != user_id:
                raise UserAlreadyExistsException(detail="Email already in use")
        if username:
            existing_username = await cls.find_one_or_none(username=username)
            if existing_username and existing_username.id != user_id:
                raise UserAlreadyExistsException(detail="Username already in use")