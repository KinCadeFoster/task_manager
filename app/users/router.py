from fastapi import APIRouter, status, Response, Depends

from app.users.dependencies import get_current_user
from app.users.models import UsersTableModel
from app.users.schemas import SchemaUserRegister, SchemaUserAuth, SchemaUser, SchemaUserUpdate, SchemaUserPasswordUpdate
from app.users.service import UsersService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: SchemaUserRegister,
        current_user: UsersTableModel = Depends(get_current_user)
) -> SchemaUser:
    return await UsersService.register_user(user_data, current_user)


@router.post("/login")
async def login_user(response: Response, user_data: SchemaUserAuth):
    return await UsersService.login_user(response, user_data)


@router.post("/logout")
async def logout_user(response: Response):
    return await UsersService.logout_user(response)


@router.patch("/{user_id}", response_model=SchemaUser)
async def update_user(
        user_id: int,
        update_user_data: SchemaUserUpdate,
        current_user: UsersTableModel = Depends(get_current_user)
):
    return await UsersService.update_user(user_id, update_user_data, current_user)


@router.get("/me")
async def read_user_me(current_user: SchemaUser = Depends(get_current_user)) -> SchemaUser:
    return current_user


@router.get("/all")
async def get_user_all(current_user: SchemaUser = Depends(get_current_user)) -> list[SchemaUser]:
    return await UsersService.get_user_all(current_user)


@router.post("/change-password", response_model=SchemaUser)
async def change_password(
        data: SchemaUserPasswordUpdate,
        current_user: UsersTableModel = Depends(get_current_user),
):
    return await UsersService.change_password(data, current_user)


@router.post("/admin-change-password/{user_id}", response_model=SchemaUser)
async def admin_change_password(
        user_id: int,
        new_password: str,
        current_user: UsersTableModel = Depends(get_current_user),
):
    return await UsersService.admin_change_password(user_id, new_password, current_user)
