from httpx import AsyncClient
import pytest
from fastapi import status

from app.tests.conftest import authenticated_user

DEFAULT_PROJECTS_COUNT = 2
USER_ADD_TO_PROJECT = 1
NON_EXISTENT_ID = 9999


def validate_project_structure(project: dict):
    """Валидация структуры проекта (статический метод)"""
    required_fields = ["id", "name", "description"]
    for field in required_fields:
        assert field in project, f"Проект должен содержать поле {field}"

    assert isinstance(project["id"], int), "ID проекта должен быть целым числом"
    assert isinstance(project["name"], str), "Название проекта должно быть строкой"
    assert isinstance(project["description"], str), "Описание проекта должно быть строкой"

class TestsGetAllProjects:
    """Тесты для get_all_projects"""

    async def test_get_all_project_manager(self, authenticated_manager: AsyncClient):
        """Менеджер получает список всех проектов"""
        response = await authenticated_manager.get("/project/")
        assert response.status_code == status.HTTP_200_OK

        projects = response.json()
        assert isinstance(projects, list), "Ответ должен быть списком"
        assert len(projects) == DEFAULT_PROJECTS_COUNT, (
            f"Ожидалось {DEFAULT_PROJECTS_COUNT} проектов, получено {len(projects)}"
        )

        for project in projects:
            validate_project_structure(project)

    async def test_get_all_project_user(self, authenticated_user: AsyncClient, authenticated_manager: AsyncClient):
        """Обычный пользователь видит только проекты на которые добавлен"""
        response = await authenticated_user.get("/project/")
        assert response.status_code == status.HTTP_200_OK

        projects = response.json()
        assert len(projects) == USER_ADD_TO_PROJECT

        for project in projects:
            validate_project_structure(project)


    async def test_get_all_project_admin(self, authenticated_admin: AsyncClient):
        """Админ получает список всех проектов"""
        response = await authenticated_admin.get("/project/")
        assert response.status_code == status.HTTP_200_OK

        projects = response.json()
        assert len(projects) == DEFAULT_PROJECTS_COUNT

        for project in projects:
            validate_project_structure(project)


class TestsGetProjectsById:
    """Тесты для get_project_by_id"""

    @pytest.mark.parametrize("project_id", [1, 2])
    async def test_get_project_by_id_by_manager(self, project_id, authenticated_manager: AsyncClient):
        """Менеджер может получить любой проект"""
        response = await authenticated_manager.get(f"/project/{project_id}")
        assert response.status_code == status.HTTP_200_OK

        project = response.json()
        validate_project_structure(project)
        assert project["id"] == project_id, "ID проекта не совпадает с запрошенным"

    async def test_get_project_by_id_by_manager_project_nonexistent(self, authenticated_manager: AsyncClient):
        """Попытка получить несуществующий проект"""
        response = await authenticated_manager.get(f"/project/{NON_EXISTENT_ID}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Project not found"}

    @pytest.mark.parametrize("project_id", [1])
    async def test_get_project_by_id_by_user(self, project_id, authenticated_user: AsyncClient):
        response = await authenticated_user.get(f"/project/{project_id}")
        assert response.status_code == 200
        project = response.json()
        validate_project_structure(project)
        assert project["id"] == project_id, "ID проекта не совпадает с запрошенным"

    @pytest.mark.parametrize("project_id", [2])
    async def test_get_project_by_id_by_user_is_not_project(
            self, project_id, authenticated_user: AsyncClient, authenticated_manager: AsyncClient
    ):
        response = await authenticated_user.get(f"/project/{project_id}")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {
            "detail": "You do not have permission to perform this action"
        }

    async def test_get_project_by_id_by_user_project_no_exist(self, authenticated_user: AsyncClient):
        """Попытка получить несуществующий проект"""
        response = await authenticated_user.get(f"/project/{NON_EXISTENT_ID}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Project not found"}

    @pytest.mark.parametrize("project_id", [1, 2])
    async def test_get_project_by_id_by_admin(self, project_id, authenticated_admin: AsyncClient):
        response = await authenticated_admin.get(f"/project/{project_id}")
        assert response.status_code == status.HTTP_200_OK

        project = response.json()
        validate_project_structure(project)
        assert project["id"] == project_id, "ID проекта не совпадает с запрошенным"

    async def test_get_project_by_id_by_admin_project_no_exist(self, authenticated_admin: AsyncClient):
        """Попытка получить несуществующий проект"""
        response = await authenticated_admin.get(f"/project/{NON_EXISTENT_ID}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Project not found"}


class TestsAddProject:
    """Тесты для add_project"""

    @pytest.mark.parametrize(
        "project_data",
        [
            {
                "name": "My Test Project",
                "prefix_name": "TST",
                "description": "Test project",
            }
        ]
    )
    async def test_add_project_manager(self, authenticated_manager: AsyncClient, project_data):
        response = await authenticated_manager.post(f"/project/", json=project_data)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        assert response_data["name"] == project_data["name"]
        assert response_data["prefix_name"] == project_data["prefix_name"]
        assert response_data["description"] == project_data["description"]


    @pytest.mark.parametrize(
        "project_data",
        [
            {
                "name": "My Test Project",
                "prefix_name": "TST",
                "description": "Test project",
            }
        ]
    )
    async def test_add_duplicate_project_manager(self, authenticated_manager: AsyncClient, project_data):
        response = await authenticated_manager.post(f"/project/", json=project_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail":"Project with this prefix name already exists"}



    @pytest.mark.parametrize(
        "project_data",
        [
            {
                "name": "My Test Project",
                "prefix_name": "TST",
                "description": "Test project",
            }
        ]
    )
    async def test_add_project_user(self, authenticated_user: AsyncClient, project_data):
        response = await authenticated_user.post(f"/project/", json=project_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'You do not have permission to perform this action'}


    @pytest.mark.parametrize(
        "project_data",
        [
            {
                "name": "My Test Project",
                "prefix_name": "TST",
                "description": "Test project",
            }
        ]
    )
    async def test_add_project_admin(self, authenticated_admin: AsyncClient, project_data):
        response = await authenticated_admin.post(f"/project/", json=project_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'You do not have permission to perform this action'}


class TestsUpdateProject:
    """Тесты для update_project"""

    @pytest.mark.parametrize(
        "update_project_data",
        [
            {
                "name": "My Update Project",
                "description": "Update project",
                "creator_id": 2
            }
        ]
    )
    async def test_update_project_manager(self, authenticated_manager: AsyncClient, update_project_data):
        response = await authenticated_manager.patch(f"/project/1", json=update_project_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()

        assert response_data["name"] == update_project_data["name"]
        assert response_data["description"] == update_project_data["description"]
        assert response_data["creator_id"] == update_project_data["creator_id"]

    @pytest.mark.parametrize(
        "update_project_data",
        [
            {
                "name": "My Update Project",
                "description": "Update project",
                "creator_id": 2
            }
        ]
    )
    async def test_update_project_no_permission_user(self, authenticated_user: AsyncClient, update_project_data):
        response = await authenticated_user.patch(f"/project/1", json=update_project_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'You do not have permission to perform this action'}

    @pytest.mark.parametrize(
        "update_project_data",
        [
            {
                "name": "My Update Project",
                "description": "Update project",
                "creator_id": 2
            }
        ]
    )
    async def test_update_project_no_permission_admin(self, authenticated_admin: AsyncClient, update_project_data):
        response = await authenticated_admin.patch(f"/project/1", json=update_project_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'You do not have permission to perform this action'}


class TestsInactivateProject:
    """Тесты для inactivate_project"""

    async def test_inactivate_project_manager(self, authenticated_manager: AsyncClient):
        get_response = await authenticated_manager.get("/project/3")
        assert get_response.status_code == status.HTTP_200_OK
        original_data = get_response.json()
        assert original_data["is_active"] is True

        patch_response = await authenticated_manager.patch("/project/inactivate/3")
        assert patch_response.status_code == status.HTTP_200_OK
        patched_data = patch_response.json()

        assert patched_data["is_active"] is False

        expected_data = original_data.copy()
        expected_data["is_active"] = False
        expected_data["updated_at"] = patched_data["updated_at"]

        assert patched_data == expected_data, (
            f"Данные проекта изменились не так, как ожидалось.\n"
            f"Ожидалось: {expected_data}\n"
            f"Получено: {patched_data}"
        )

        verify_response = await authenticated_manager.get("/project/3")
        assert verify_response.json() == expected_data

    async def test_inactivate_nonexistent_project(self, authenticated_manager):
        response = await authenticated_manager.patch(f"/project/inactivate/{NON_EXISTENT_ID}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_inactivate_project_no_permission_user(self, authenticated_user):
        response = await authenticated_user.patch("/project/inactivate/1")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_inactivate_project_no_permission_admin(self, authenticated_admin):
        response = await authenticated_admin.patch("/project/inactivate/1")
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestsDeleteProject:
    """Тесты для delete_project"""

    async def test_delete_project_by_admin(self, authenticated_admin):
        """Админ может удалить любой неактивный проект"""
        project_id = 3
        response = await authenticated_admin.delete(f"/project/{project_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_delete_project_by_non_admin(self, authenticated_manager, authenticated_user):
        response_manager = await authenticated_manager.delete(f"/project/2")
        assert response_manager.status_code == status.HTTP_403_FORBIDDEN
        response_user = await authenticated_user.delete(f"/project/2")
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

    async def test_delete_no_exist_project_by_admin(self, authenticated_admin):
        response = await authenticated_admin.delete(f"/project/3")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_no_exist_project_by_non_admin(self, authenticated_manager, authenticated_user):
        response_manager = await authenticated_manager.delete(f"/project/3")
        assert response_manager.status_code == status.HTTP_404_NOT_FOUND
        response_user = await authenticated_manager.delete(f"/project/3")
        assert response_user.status_code == status.HTTP_404_NOT_FOUND


class TestsGetProjectUsers:
    """Тесты для get_project_users"""

    async def test_get_project_users_by_manager(self, authenticated_manager):
        project_id = 1
        response = await authenticated_manager.get(f"/project/{project_id}/users")
        assert response.status_code == status.HTTP_200_OK

    async def test_get_project_users_by_admin(self, authenticated_admin):
        project_id = 1
        response = await authenticated_admin.get(f"/project/{project_id}/users")
        assert response.status_code == status.HTTP_200_OK

    async def test_get_project_users_by_user(self, authenticated_user):
        project_id = 1
        response = await authenticated_user.get(f"/project/{project_id}/users")
        assert response.status_code == status.HTTP_200_OK


class TestsUsersToProject:
    """Тесты для add_user_to_project"""

    async def test_add_project_users_to_project_by_manager(self, authenticated_manager):
        project_id = 2
        user_id = 3
        response = await authenticated_manager.post(f"/project/{project_id}/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK


class TestsRemoveUsersFromProject:
    """Тесты для remove_user_from_project"""

    async def test_remove_user_from_project_by_manager(self, authenticated_manager):
        project_id = 2
        user_id = 3
        response = await authenticated_manager.delete(f"/project/{project_id}/users/{user_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT


    async def test_remove_user_no_exist_from_project_by_manager(self, authenticated_manager):
        project_id = 2
        user_id = NON_EXISTENT_ID
        response = await authenticated_manager.delete(f"/project/{project_id}/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND