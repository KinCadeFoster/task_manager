from fastapi import APIRouter, status, HTTPException, Depends

from app.comments.dependencies import check_user_can_access_task_for_manager_or_user
from app.comments.schemas import SchemaComment, SchemaCommentAdd, SchemaCommentUpdate
from app.comments.service import CommentService
from app.exceptions import UserPermissionError
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel

router = APIRouter(prefix="/comments",tags=["Comments"])

@router.get("/", response_model=list[SchemaComment])
async def get_all_comment(current_user: UsersTableModel = Depends(get_current_user)):
    if not (current_user.is_manager or current_user.is_user):
        raise UserPermissionError
    return await CommentService.find_all()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SchemaComment)
async def add_comment(
    new_comment: SchemaCommentAdd,
    current_user: UsersTableModel = Depends(get_current_user)
):
    await check_user_can_access_task_for_manager_or_user(new_comment.task_id, current_user)
    return await CommentService.add(**new_comment.model_dump())

@router.patch("/{comment_id}", response_model=SchemaComment)
async def update_comment(
    comment_id: int,
    data: SchemaCommentUpdate,
    current_user: UsersTableModel = Depends(get_current_user)
):
    comment = await CommentService.find_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await check_user_can_access_task_for_manager_or_user(comment.task_id, current_user)
    updated_comment = await CommentService.update_by_id(comment_id, **data.model_dump(exclude_unset=True))
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: UsersTableModel = Depends(get_current_user)
):
    comment = await CommentService.find_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await check_user_can_access_task_for_manager_or_user(comment.task_id, current_user)
    result = await CommentService.delete_by_id(comment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")
    return None

@router.get("/comments-by-task/{task_id}", response_model=list[SchemaComment])
async def get_comments_by_task(
    task_id: int,
    current_user: UsersTableModel = Depends(get_current_user)
):
    await check_user_can_access_task_for_manager_or_user(task_id, current_user)
    return await CommentService.find_all(task_id=task_id)