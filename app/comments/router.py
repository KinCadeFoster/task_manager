from fastapi import APIRouter, status, HTTPException
from app.comments.schemas import SchemaComment, SchemaCommentAdd, SchemaCommentUpdate
from app.comments.service import CommentService

router = APIRouter(prefix="/comments",tags=["Comments"])

@router.get("/")
async def get_all_comment() -> list[SchemaComment]:
    return await CommentService.find_all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_comment(new_comment: SchemaCommentAdd) -> SchemaComment:
    return await CommentService.add(**new_comment.model_dump()
    )

@router.patch("/{comment_id}")
async def update_comment(comment_id: int, data: SchemaCommentUpdate) -> SchemaComment:
    comment = await CommentService.update_by_id(comment_id, **data.model_dump())
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int):
    result = await CommentService.delete_by_id(comment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")
    return None