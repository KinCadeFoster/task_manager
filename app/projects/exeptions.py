from fastapi import HTTPException, status

UserAlreadyInProject = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="User already in project",
)

CannotRemoveCreator = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Cannot remove project creator from project",
)

UserNotInProject = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User not in project",
)

NewCreatorNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="New creator not found",
)

NewCreatorMustBeManager = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="New creator must be a manager",
)

ProjectAlreadyInactive = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Project already inactive",
)

ProjectMustBeInactive = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Project must be inactive before deletion",
)