from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import UserAdmin, ProjectAdmin, TaskAdmin, CommentAdmin
from app.database import engine

from app.initial_data import init_db
from app.projects.router import router as router_projects
from app.tasks.router import router as router_tasks
from app.comments.router import router as router_comments
from app.users.router import router as router_users

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(router_tasks)
app.include_router(router_projects)
app.include_router(router_comments)
app.include_router(router_users)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(ProjectAdmin)
admin.add_view(TaskAdmin)
admin.add_view(CommentAdmin)