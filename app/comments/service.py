from app.service.base import BaseService
from app.comments.models import CommentTableModel


class CommentService(BaseService):
    model = CommentTableModel