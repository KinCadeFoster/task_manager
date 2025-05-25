from fastapi import APIRouter, HTTPException, status, Response

from app.users.schemas import SchemaUserRegister, SchemaUserAuth
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.service import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
async def register_user(user_data: SchemaUserRegister):
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    existing_username = await UsersService.find_one_or_none(username=user_data.username)
    if existing_user or existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(
        email=user_data.email,
        hash_password=hashed_password,
        name=user_data.name,
        surname=user_data.surname,
        patronymic=user_data.patronymic,
        username=user_data.username
    )

@router.post("/login")
async def login_user(response: Response, user_data: SchemaUserAuth):
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("task_manager_access_token", access_token, httponly=True)
    return access_token