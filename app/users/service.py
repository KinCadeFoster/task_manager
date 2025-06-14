from app.exceptions import UserAlreadyExistsException, IncorrectUsernameOrPasswordException
from app.service.base import BaseService
from app.users.hashing import verify_password, get_password_hash
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

    @classmethod
    async def update_password(cls, user_id: int, old_password: str, new_password: str):
        user = await cls.find_by_id(user_id)
        if not user or not verify_password(old_password, user.hash_password):
            raise IncorrectUsernameOrPasswordException(detail="Current password is incorrect")
        new_hash = get_password_hash(new_password)
        await UsersService.update_by_id(user_id, hash_password=new_hash)
        updated_user = await cls.find_by_id(user_id)
        return updated_user