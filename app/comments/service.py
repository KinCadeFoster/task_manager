from app.comments.dependencies import check_access_for_comments
from app.comments.exeptions import CommentNotFound, CommentNoPermission
from app.comments.schemas import SchemaCommentUpdate, SchemaCommentAdd
from app.service.base import BaseService
from app.comments.models import CommentTableModel
from app.users.models import UsersTableModel


class CommentService(BaseService):
    model = CommentTableModel

    @classmethod
    async def add_comment(cls, new_comment: SchemaCommentAdd, current_user: UsersTableModel):
        await check_access_for_comments(new_comment.task_id, current_user)
        return await CommentService.add(**new_comment.model_dump(), creator_id=current_user.id)

    @classmethod
    async def update_comment(cls, comment_id: int, data: SchemaCommentUpdate, current_user: UsersTableModel):
        comment = await CommentService.find_by_id(comment_id)
        if not comment:
            raise CommentNotFound
        if comment.creator_id != current_user.id:
            raise CommentNoPermission
        await check_access_for_comments(comment.task_id, current_user)
        updated_comment = await CommentService.update_by_id(comment_id, **data.model_dump(exclude_unset=True))
        if not updated_comment:
            raise CommentNotFound
        else:
            return updated_comment

    @classmethod
    async def delete_comment(cls, comment_id: int, current_user: UsersTableModel):
        comment = await CommentService.find_by_id(comment_id)
        if not comment:
            raise CommentNotFound
        if comment.creator_id != current_user.id:
            raise CommentNoPermission
        await check_access_for_comments(comment.task_id, current_user)
        result = await CommentService.delete_by_id(comment_id)
        if not result:
            raise CommentNotFound
        return None

    @classmethod
    async def get_comments_by_task_id(cls, task_id: int, current_user: UsersTableModel):
        await check_access_for_comments(task_id, current_user)
        return await CommentService.find_all(task_id=task_id)