from datetime import datetime, UTC
from fastapi import Request, Depends
from jose import jwt, JWTError
from app.config import settings
from app.exceptions import UserPermissionError, UserIsNotPresentException, TokenExpiredException, \
    IncorrectTokenFormatException, TokenAbsentException
from app.users.schemas import SchemaUser
from app.users.service import UsersService


def get_token(request: Request):
    token = request.cookies.get("task_manager_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersService.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user

async def get_current_admin_user(current_user: SchemaUser = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise UserPermissionError