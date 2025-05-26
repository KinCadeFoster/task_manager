from fastapi import APIRouter
from app.comments.schemas import SchemaComment, SchemaCommentAdd, SchemaCommentUpdate
from app.comments.service import CommentService

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.get("")
async def get_all_comment() -> list[SchemaComment]:
    return await CommentService.find_all()

@router.post("")
async def add_comment(new_comment: SchemaCommentAdd) -> SchemaComment:
    return await CommentService.add(
        task_id=new_comment.task_id,
        creator_id=new_comment.creator_id,
        comment_text=new_comment.comment_text
    )

@router.patch("")
async def update_comment(data: SchemaCommentUpdate) -> SchemaComment:
    return await CommentService.update_by_id(data.id, comment_text=data.comment_text)

@router.delete("")
async def delete_comment(id_comment: int):
    return await CommentService.delete_by_id(id_comment)