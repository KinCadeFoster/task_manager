import os


os.environ["MODE"] = "TEST"

import asyncio
import json

import pytest
from sqlalchemy import insert

from app.database import Base, async_session_maker, engine
from app.config import settings

from app.projects.models import ProjectTableModel
from app.tasks.models import TaskTableModel
from app.users.models import UsersTableModel
from app.comments.models import CommentTableModel

from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app as fastapi_app

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_data/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    projects = open_mock_json("projects")
    tasks = open_mock_json("tasks")
    comments = open_mock_json("comments")

    async with async_session_maker() as session:
        add_users = insert(UsersTableModel).values(users)
        add_projects = insert(ProjectTableModel).values(projects)
        add_tasks = insert(TaskTableModel).values(tasks)
        add_comments = insert(CommentTableModel).values(comments)

        await session.execute(add_users)
        await session.execute(add_projects)
        await session.execute(add_tasks)
        await session.execute(add_comments)

        await session.commit()

@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def authenticated_admin():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "username": "admin",
            "password": "admin"
        })
        assert ac.cookies["task_manager_access_token"]
        yield ac

@pytest.fixture(scope="session")
async def authenticated_manager():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "username": "string",
            "password": "string"
        })
        assert ac.cookies["task_manager_access_token"]
        yield ac

@pytest.fixture(scope="session")
async def authenticated_user():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "username": "user",
            "password": "string"
        })
        assert ac.cookies["task_manager_access_token"]
        yield ac

