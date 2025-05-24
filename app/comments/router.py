from fastapi import APIRouter
from app.comments.schemas import SchemaComment, SchemaCommentAdd

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.get("/comment")
async def get_all_comment() -> list[SchemaComment]:
    return "status: OK"

@router.post("/comment")
async def add_comment(new_comment: SchemaCommentAdd):
    return "status: OK"