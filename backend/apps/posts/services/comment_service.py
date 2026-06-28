from apps.core.enums import UserRole
from apps.core.exceptions import PermissionDeniedException
from apps.posts.models import Comment
from apps.posts.repositories.comment_repository import CommentRepository
from apps.posts.repositories.post_repository import PostRepository


class CommentService:
    """Singleton service for comment business logic."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "CommentService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self._comment_repository = CommentRepository.get_instance()
        self._post_repository = PostRepository.get_instance()

    def add_comment(self, post_slug: str, author, content: str) -> Comment:
        post = self._post_repository.get_by_slug(post_slug)
        return self._comment_repository.create(post=post, author=author, content=content)

    def delete_comment(self, comment_id: int, requesting_user) -> None:
        comment = self._comment_repository.get_by_id(comment_id)
        if comment.author != requesting_user and requesting_user.role != UserRole.ADMIN:
            raise PermissionDeniedException("Cannot delete another user's comment")
        self._comment_repository.delete(comment)
