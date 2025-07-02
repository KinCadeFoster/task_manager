
from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("username,password, status_code",[
    ("admin", "admin", 200),
    ("string", "string", 200),
    ("admin", "admin1", 401),
])

async def test_login_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "username": username,
        "password": password
    })
    assert response.status_code == status_code

@pytest.mark.parametrize(
    "email, password, surname, name, patronymic, username, is_admin, is_manager, is_user, status_code",
    [
        ("integation@test.com", "password", "Integration", "Petr", "Ivanovich", "Integration", False, True, True, 201),
        ("integation@test.com", "password", "Integration", "Petr", "Ivanovich", "Integration", False, True, True, 400),
        ("integation@test", "password", "Integration", "Petr", "Ivanovich", "Integration", False, True, True, 422),
    ]
)

async def test_registration_new_user(
        email, password, surname, name, patronymic, username, is_admin, is_manager,
        is_user, status_code, authenticated_admin:AsyncClient
):
    response = await authenticated_admin.post("/auth/register", json={
    "email": email,
    "password": password,
    "name": name,
    "surname": surname,
    "patronymic": patronymic,
    "username": username,
    "is_admin": is_admin,
    "is_manager": is_manager,
    "is_user": is_user
})

    assert response.status_code == status_code