from fastapi import APIRouter
from app.comments.schemas import SchemaComment, SchemaCommentAdd
from app.comments.service import CommentService

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.get("")
async def get_all_comment() -> list[SchemaComment]:
    return await CommentService.find_all()

@router.post("")
async def add_comment(new_comment: SchemaCommentAdd):
    await CommentService.add(
        task_id=new_comment.task_id,
        creator_id=new_comment.creator_id,
        comment_text=new_comment.comment_text
    )