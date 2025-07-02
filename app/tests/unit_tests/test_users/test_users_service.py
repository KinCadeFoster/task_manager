import pytest

from app.users.service import UsersService

@pytest.mark.parametrize("user_id, email, surname, patronymic, username, is_admin, is_manager, is_user",[
    (1, "admin@admin.ru", "admin", "admin", "admin", True, False, False),
    (2, "manager@example.com", "String", "String" , "string", False, True, False)
])

async def test_find_user_by_id(user_id, email, surname, patronymic, username, is_admin, is_manager, is_user):
    user = await UsersService.find_by_id(user_id)

    assert user.id == user_id
    assert user.email == email
    assert user.surname == surname
    assert user.patronymic == patronymic
    assert user.username == username
    assert user.is_admin == is_admin
    assert user.is_manager == is_manager
    assert user.is_user == is_user

async def test_find_user_by_id_not_found():
    user = await UsersService.find_by_id(99999)  # id, который точно не существует
    assert user is None