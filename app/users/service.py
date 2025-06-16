from fastapi import Response

from app.exceptions import UserAlreadyExistsException, IncorrectUsernameOrPasswordException, UserPermissionError
from app.service.base import BaseService
from app.users.auth import authenticate_user
from app.users.exeptions import UserNotFound
from app.users.hashing import verify_password, get_password_hash
from app.users.jwt_utils import create_access_token
from app.users.models import UsersTableModel
from app.users.schemas import SchemaUserRegister, SchemaUserAuth, SchemaUserUpdate, SchemaUser, SchemaUserPasswordUpdate


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

    @classmethod
    async def register_user(cls, user_data: SchemaUserRegister, current_user: UsersTableModel):
        if not current_user.is_admin:
            raise UserPermissionError

        existing_user = await UsersService.find_one_or_none(email=user_data.email)
        existing_username = await UsersService.find_one_or_none(username=user_data.username)
        if existing_user or existing_username:
            raise UserAlreadyExistsException

        hashed_password = get_password_hash(user_data.password)
        user_dict = user_data.model_dump(exclude={"password"})
        user = await UsersService.add(hash_password=hashed_password, **user_dict)
        return user

    @classmethod
    async def login_user(cls, response: Response, user_data: SchemaUserAuth):
        user = await authenticate_user(user_data.username, user_data.password)
        if not user:
            raise IncorrectUsernameOrPasswordException
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("task_manager_access_token", access_token, httponly=True)
        return {"access_token": access_token, "token_type": "bearer"}

    @classmethod
    async def logout_user(cls, response: Response):
        response.delete_cookie("task_manager_access_token")
        return {"detail": "Logged out successfully."}

    @classmethod
    async def update_user(cls, user_id: int, update_user_data: SchemaUserUpdate, current_user: UsersTableModel):
        if not current_user.is_admin:
            raise UserPermissionError
        user_obj = await UsersService.find_by_id(user_id)
        if not user_obj:
            raise UserNotFound
        update_dict = update_user_data.model_dump(exclude_unset=True)
        email = update_dict.get("email")
        username = update_dict.get("username")
        await UsersService.check_unique_fields_on_update(user_id, email=email, username=username)

        user = await UsersService.update_by_id(user_id, **update_user_data.model_dump(exclude_unset=True))
        return user

    @classmethod
    async def get_user_all(cls, current_user: SchemaUser):
        if not current_user.is_admin:
            raise UserPermissionError
        return await UsersService.find_all()

    @classmethod
    async def change_password(cls, data: SchemaUserPasswordUpdate, current_user: UsersTableModel):
        user = await UsersService.update_password(
            user_id=current_user.id,
            old_password=data.old_password,
            new_password=data.new_password
        )
        return user

    @classmethod
    async def admin_change_password(cls, user_id: int, new_password: str, current_user: UsersTableModel):
        if not current_user.is_admin:
            raise UserPermissionError
        user = await UsersService.find_by_id(user_id)
        if not user:
            raise UserNotFound
        new_hash = get_password_hash(new_password)
        updated_user = await UsersService.update_by_id(user_id, hash_password=new_hash)
        return updated_user
