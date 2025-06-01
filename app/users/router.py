from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectUsernameOrPasswordException
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.schemas import SchemaUserRegister, SchemaUserAuth, SchemaUser
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.service import UsersService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SchemaUserRegister) -> SchemaUser:
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    existing_username = await UsersService.find_one_or_none(username=user_data.username)
    if existing_user or existing_username:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump(exclude={"password"})
    user = await UsersService.add(hash_password=hashed_password, **user_dict)
    return user

@router.post("/login")
async def login_user(response: Response, user_data: SchemaUserAuth):
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise IncorrectUsernameOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("task_manager_access_token", access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def login_user(response: Response):
    response.delete_cookie("task_manager_access_token")
    return {"detail": "Logged out successfully."}

@router.get("/me")
async def read_user_me(current_user: SchemaUser = Depends(get_current_user)):
    return current_user

@router.get("/all")
async def read_user_all(current_user: SchemaUser = Depends(get_current_admin_user)) -> list[SchemaUser]:
    return await UsersService.find_all()