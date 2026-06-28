from apps.core.enums import PostStatus, UserRole
from apps.core.exceptions import NotFoundException, PermissionDeniedException, ValidationException
from apps.posts.models import Category, Post
from apps.posts.repositories.post_repository import PostRepository


class PostService:
    """Singleton service containing post business logic."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "PostService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self._post_repository = PostRepository.get_instance()

    def get_feed(self, user=None, search: str = "", category_slug: str = ""):
        return self._post_repository.get_feed(user=user, search=search, category_slug=category_slug)

    def get_post(self, slug: str) -> Post:
        return self._post_repository.get_by_slug(slug)

    def get_user_posts(self, user):
        return self._post_repository.get_user_posts(user)

    def get_all_posts(self):
        return self._post_repository.get_all()

    def create_post(self, author, validated_data: dict) -> Post:
        tag_names = validated_data.pop("tag_names", [])
        category_id = validated_data.pop("category_id", None)
        cover_image = validated_data.pop("cover_image", None)

        category_obj = self._resolve_category(category_id)
        post = self._post_repository.create(
            author=author,
            category=category_obj,
            cover_image=cover_image,
            **validated_data,
        )
        if tag_names:
            self._post_repository.set_tags(post, tag_names)
        return post

    def update_post(self, slug: str, requesting_user, validated_data: dict) -> Post:
        post = self._post_repository.get_by_slug(slug)
        self._assert_can_modify(post, requesting_user)

        tag_names = validated_data.pop("tag_names", None)
        category_id = validated_data.pop("category_id", None)

        if category_id is not None:
            validated_data["category"] = self._resolve_category(category_id)

        updated_post = self._post_repository.update(post, **validated_data)
        if tag_names is not None:
            self._post_repository.set_tags(updated_post, tag_names)
        return updated_post

    def delete_post(self, slug: str, requesting_user) -> None:
        post = self._post_repository.get_by_slug(slug)
        self._assert_can_modify(post, requesting_user)
        self._post_repository.delete(post)

    def record_view(self, post_id: int) -> None:
        self._post_repository.increment_views(post_id)

    def _resolve_category(self, category_id: int | None) -> Category | None:
        if not category_id:
            return None
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return None

    def _assert_can_modify(self, post: Post, user) -> None:
        if post.author != user and user.role != UserRole.ADMIN:
            raise PermissionDeniedException("You do not have permission to modify this post")
