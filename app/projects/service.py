
from app.projects.models import ProjectTableModel
from app.service.base import BaseService


class ProjectService(BaseService):
    model = ProjectTableModel