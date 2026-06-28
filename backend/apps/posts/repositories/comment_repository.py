
from apps.core.exceptions import NotFoundException
from apps.posts.models import Comment


class CommentRepository:
    """Singleton repository for Comment ORM queries."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "CommentRepository":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create(self, post, author, content: str) -> Comment:
        return Comment.objects.create(post=post, author=author, content=content)

    def get_by_id(self, comment_id: int) -> Comment:
        try:
            return Comment.objects.select_related("author", "post").get(pk=comment_id)
        except Comment.DoesNotExist as exc:
            raise NotFoundException(f"Comment {comment_id} not found") from exc

    def delete(self, comment: Comment) -> None:
        comment.delete()
