from sqladmin import ModelView


from app.comments.models import CommentTableModel
from app.projects.models import ProjectTableModel
from app.tasks.models import TaskTableModel
from app.users.models import UsersTableModel


class UserAdmin(ModelView, model=UsersTableModel):
    column_list = [c.name for c in UsersTableModel.__table__.c]
    form_columns = ["email", "name", "surname", "patronymic", "username", "is_admin", "is_manager", "is_user"]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    can_delete = False
    can_create = False

class ProjectAdmin(ModelView, model=ProjectTableModel):
    column_list = [c.name for c in ProjectTableModel.__table__.c]
    form_columns = ["name", "prefix_name", "description", "creator_id", "is_active"]
    name = "Проект"
    name_plural = "Проекты"

class TaskAdmin(ModelView, model=TaskTableModel):
    column_list = [c.name for c in TaskTableModel.__table__.c]
    form_columns = ["name", "description", "project_id", "creator_id", "assignee_id", "priority", "status"]
    name = "Задачи"
    name_plural = "Задачи"
    can_create = False

class CommentAdmin(ModelView, model=CommentTableModel):
    column_list = [c.name for c in CommentTableModel.__table__.c]
    form_columns = ["creator_id", "comment_text", "task_id", "is_deleted"]
    name = "Комментарий"
    name_plural = "Комментарии"
    can_create = False