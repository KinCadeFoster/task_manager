from app.projects.service import ProjectService
from app.exceptions import UserPermissionError, UserIsNotMemberProject
from app.users.models import UsersTableModel

async def check_access_for_tasks(
    project_id,
    current_user: UsersTableModel
):
    if not (current_user.is_manager or current_user.is_user):
        raise UserPermissionError
    in_project = await ProjectService.user_in_project(project_id, current_user.id)
    if not in_project:
        raise UserIsNotMemberProject
    return current_user