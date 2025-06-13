from datetime import datetime, UTC
from fastapi import Request, Depends, HTTPException
from jose import jwt, JWTError
from app.config import settings
from app.exceptions import UserPermissionError, UserIsNotPresentException, TokenExpiredException, \
    IncorrectTokenFormatException, TokenAbsentException
from app.projects.service import ProjectService
from app.tasks.service import TaskService
from app.users.models import UsersTableModel
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

async def check_user_can_access_task_for_manager_or_user(
    task_id: int,
    current_user: UsersTableModel
):
    if not (current_user.is_manager or current_user.is_user):
        raise UserPermissionError
    project_id = await TaskService.get_project_id_by_task_id(task_id)
    in_project = await ProjectService.user_in_project(project_id, current_user.id)
    if not in_project:
        raise HTTPException(status_code=403, detail="User not in project")
    return True