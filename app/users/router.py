from fastapi import APIRouter, HTTPException

from app.users.schemas import SchemaUserRegister
from app.users.auth import get_password_hash
from app.users.service import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register")
async def register_user(user_data: SchemaUserRegister):
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    existing_username = await UsersService.find_one_or_none(username=user_data.username)
    if existing_user or existing_username:
        raise HTTPException(status_code=409)
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(
        email=user_data.email,
        hash_password=hashed_password,
        name=user_data.name,
        surname=user_data.surname,
        patronymic=user_data.patronymic,
        username=user_data.username
    )