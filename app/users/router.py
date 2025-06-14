from fastapi import APIRouter, status, Response, Depends, HTTPException

from app.exceptions import UserAlreadyExistsException, IncorrectUsernameOrPasswordException, UserPermissionError
from app.users.dependencies import get_current_user, get_current_admin_user, check_user_can_access_for_admin
from app.users.models import UsersTableModel
from app.users.schemas import SchemaUserRegister, SchemaUserAuth, SchemaUser, SchemaUserUpdate
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.service import UsersService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: SchemaUserRegister,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaUser:
    # Проверка прав
    if not current_user.is_admin:
        raise UserPermissionError

    # Проверка уникальности пользователя
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    existing_username = await UsersService.find_one_or_none(username=user_data.username)
    if existing_user or existing_username:
        raise UserAlreadyExistsException

    # Хешируем пароль и создаём пользователя
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

@router.patch("/{user_id}", response_model=SchemaUser)
async def update_user(
    user_id: int,
    update_user_data: SchemaUserUpdate,
    current_user: UsersTableModel = Depends(get_current_user)
):
    await check_user_can_access_for_admin(user_id, current_user)
    update_dict = update_user_data.model_dump(exclude_unset=True)
    email = update_dict.get("email")
    username = update_dict.get("username")
    await UsersService.check_unique_fields_on_update(user_id, email=email, username=username)

    user = await UsersService.update_by_id(user_id, **update_user_data.model_dump(exclude_unset=True))
    return user

@router.get("/me")
async def read_user_me(current_user: SchemaUser = Depends(get_current_user)) -> SchemaUser:
    return current_user

@router.get("/all")
async def read_user_all(current_user: SchemaUser = Depends(get_current_admin_user)) -> list[SchemaUser]:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have enough rights")
    return await UsersService.find_all()