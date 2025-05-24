from app.service.base import BaseService
from app.users.models import UsersTableModel


class UsersService(BaseService):
    model = UsersTableModel