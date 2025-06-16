from fastapi import HTTPException, status

CommentNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Comment not found",
)

CommentNoPermission = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No permission to update comment",
)