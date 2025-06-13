from fastapi import Depends, HTTPException
from app.users.dependencies import get_current_user
from app.projects.service import ProjectService
from app.exceptions import UserPermissionError
from app.users.models import UsersTableModel

async def check_user_can_access_task_for_manager_or_user_tasks(
    project_id,
    current_user: UsersTableModel = Depends(get_current_user)
):
    if not (current_user.is_manager or current_user.is_user):
        raise UserPermissionError
    in_project = await ProjectService.user_in_project(project_id, current_user.id)
    if not in_project:
        raise HTTPException(status_code=403, detail="User not in project")
    return current_user