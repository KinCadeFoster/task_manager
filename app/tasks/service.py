from app.service.base import BaseService
from app.tasks.models import TaskTableModel


class TaskService(BaseService):
    model = TaskTableModel