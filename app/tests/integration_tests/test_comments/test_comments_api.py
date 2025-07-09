
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("task_id, comment_text, status_code, project_id, user_id",[
    (1, "admin", 201, 1, 2),
    (2, "string", 201, 1, 2),
])

async def test_add_comment_manager(task_id, comment_text, status_code, project_id, user_id,
                                   ac: AsyncClient, authenticated_manager: AsyncClient):
    response = await authenticated_manager.post(f"/project/{project_id}/users/{user_id}")
    assert response.status_code == 200

    response = await authenticated_manager.post("/comments/", json={
        "task_id": 1,
        "comment_text": comment_text
    })
    assert response.status_code == status_code

@pytest.mark.parametrize("task_id, comment_text, status_code, project_id, user_id",[
    (1, "admin", 201, 1, 3),
    (2, "string", 201, 1, 3),
])

async def test_add_comment_user(task_id, comment_text, status_code, project_id, user_id,
                                   ac: AsyncClient, authenticated_user: AsyncClient, authenticated_manager: AsyncClient):
    response = await authenticated_manager.post(f"/project/{project_id}/users/{user_id}")
    assert response.status_code == 200

    response = await authenticated_user.post("/comments/", json={
        "task_id": 1,
        "comment_text": comment_text
    })
    assert response.status_code == status_code