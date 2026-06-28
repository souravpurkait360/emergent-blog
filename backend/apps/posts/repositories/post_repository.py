import os

from django.db.models import F, Q, QuerySet
from django.utils.text import slugify

from apps.core.enums import PostStatus
from apps.core.exceptions import NotFoundException
from apps.posts.models import Post, Tag

BACKEND_URL = os.environ.get("FRONTEND_URL", "")


class PostRepository:
    """Singleton repository for Post ORM queries."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "PostRepository":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _base_queryset(self) -> QuerySet:
        return Post.objects.select_related("author", "category").prefetch_related("tags", "comments__author")

    def get_feed(self, user=None, search: str = "", category_slug: str = "") -> QuerySet:
        """Return visible posts: published + author's own drafts."""
        queryset = self._base_queryset()
        if user and user.is_authenticated:
            queryset = queryset.filter(Q(status=PostStatus.PUBLISHED) | Q(author=user))
        else:
            queryset = queryset.filter(status=PostStatus.PUBLISHED)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset.order_by("-created_at")

    def get_by_slug(self, slug: str) -> Post:
        try:
            return self._base_queryset().get(slug=slug)
        except Post.DoesNotExist as exc:
            raise NotFoundException(f"Post '{slug}' not found") from exc

    def get_by_id(self, post_id: int) -> Post:
        try:
            return self._base_queryset().get(pk=post_id)
        except Post.DoesNotExist as exc:
            raise NotFoundException(f"Post with id {post_id} not found") from exc

    def get_all(self) -> QuerySet:
        return self._base_queryset().order_by("-created_at")

    def get_user_posts(self, user) -> QuerySet:
        return self._base_queryset().filter(author=user).order_by("-created_at")

    def create(self, author, title: str, content: str, **kwargs) -> Post:
        return Post.objects.create(author=author, title=title, content=content, **kwargs)

    def update(self, post: Post, **fields) -> Post:
        for field_name, field_value in fields.items():
            setattr(post, field_name, field_value)
        post.save()
        return post

    def delete(self, post: Post) -> None:
        post.delete()

    def increment_views(self, post_id: int) -> None:
        Post.objects.filter(pk=post_id).update(views=F("views") + 1)

    def set_tags(self, post: Post, tag_names: list[str]) -> None:
        """Bulk-create and set tags on a post - avoids N+1 queries."""
        tags = []
        for tag_name in tag_names:
            clean_name = tag_name.strip()
            if clean_name:
                tag_obj, _ = Tag.objects.get_or_create(
                    name=clean_name,
                    defaults={"slug": slugify(clean_name)},
                )
                tags.append(tag_obj)
        post.tags.set(tags)
