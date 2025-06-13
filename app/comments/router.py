from fastapi import APIRouter, status, HTTPException, Depends

from app.comments.schemas import SchemaComment, SchemaCommentAdd, SchemaCommentUpdate
from app.comments.service import CommentService
from app.exceptions import UserPermissionError
from app.tasks.service import TaskService
from app.projects.service import ProjectService
from app.users.dependencies import get_current_user, check_user_can_access_task_for_manager_or_user
from app.users.models import UsersTableModel

router = APIRouter(prefix="/comments",tags=["Comments"])

@router.get("/")
async def get_all_comment(current_user: UsersTableModel = Depends(get_current_user)) -> list[SchemaComment]:
    if not (current_user.is_manager or current_user.is_user):
        raise UserPermissionError
    return await CommentService.find_all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_comment(
    new_comment: SchemaCommentAdd,
    current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaComment:
    # Получаем project_id по task_id
    project_id = await TaskService.get_project_id_by_task_id(new_comment.task_id)
    if not project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    # Проверяем, состоит ли пользователь в проекте
    await check_user_can_access_task_for_manager_or_user(new_comment.task_id, current_user)
    # Создаём комментарий
    return await CommentService.add(**new_comment.model_dump())

@router.patch("/{comment_id}")
async def update_comment(
    comment_id: int,
    data: SchemaCommentUpdate,
    current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaComment:
    # Проверка роли пользователя
    if not (current_user.is_manager or current_user.is_user):
        raise UserPermissionError
    # Получаем комментарий
    comment = await CommentService.find_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    # Получаем project_id через task_id
    project_id = await TaskService.get_project_id_by_task_id(comment.task_id)
    if not project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    # Проверяем, состоит ли пользователь в проекте
    in_project = await ProjectService.user_in_project(project_id, current_user.id)
    if not in_project:
        raise HTTPException(status_code=403, detail="User not in project")
    # Обновляем комментарий
    updated_comment = await CommentService.update_by_id(comment_id, **data.model_dump())
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: UsersTableModel = Depends(get_current_user)
):
    # Проверка прав пользователя
    if not (current_user.is_manager or current_user.is_user):
        raise UserPermissionError
    # Получаем комментарий
    comment = await CommentService.find_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    # Получаем project_id через task_id комментария
    project_id = await TaskService.get_project_id_by_task_id(comment.task_id)
    if not project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    # Проверяем, состоит ли пользователь в проекте
    in_project = await ProjectService.user_in_project(project_id, current_user.id)
    if not in_project:
        raise HTTPException(status_code=403, detail="User not in project")
    # Удаляем комментарий
    result = await CommentService.delete_by_id(comment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")
    return None

@router.get("/by-task/{task_id}")
async def get_comments_by_task(
    task_id: int,
    current_user: UsersTableModel = Depends(get_current_user)
) -> list[SchemaComment]:
    # Проверка роли пользователя
    if not (current_user.is_manager or current_user.is_user):
        raise UserPermissionError
    # Проверяем, существует ли задача
    task = await TaskService.find_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Получаем project_id по task_id
    project_id = await TaskService.get_project_id_by_task_id(task_id)
    if not project_id:
        raise HTTPException(status_code=404, detail="Project not found")
    # Проверяем, состоит ли пользователь в проекте
    in_project = await ProjectService.user_in_project(project_id, current_user.id)
    if not in_project:
        raise HTTPException(status_code=403, detail="User not in project")
    return await CommentService.find_all(task_id=task_id)