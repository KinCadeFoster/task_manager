from fastapi import APIRouter, status, Depends
from app.comments.schemas import SchemaComment, SchemaCommentAdd, SchemaCommentUpdate
from app.comments.service import CommentService
from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SchemaComment)
async def add_comment(
        new_comment: SchemaCommentAdd,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await CommentService.add_comment(new_comment=new_comment, current_user=current_user)


@router.patch("/{comment_id}", response_model=SchemaComment)
async def update_comment(
        comment_id: int,
        data: SchemaCommentUpdate,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await CommentService.update_comment(comment_id=comment_id, data=data, current_user=current_user)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        comment_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await CommentService.delete_comment(comment_id=comment_id, current_user=current_user)


@router.get("/comments-by-task/{task_id}", response_model=list[SchemaComment])
async def get_comments_by_task(
        task_id: int,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await CommentService.get_comments_by_task(task_id=task_id, current_user=current_user)