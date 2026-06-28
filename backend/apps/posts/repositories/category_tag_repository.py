from django.db.models import QuerySet
from django.utils.text import slugify

from apps.core.exceptions import NotFoundException
from apps.posts.models import Category, Tag


class CategoryRepository:
    """Singleton repository for Category ORM queries."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "CategoryRepository":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_all(self) -> QuerySet:
        return Category.objects.all().order_by("name")

    def create(self, name: str, description: str = "") -> Category:
        return Category.objects.create(name=name, description=description)

    def get_by_slug(self, slug: str) -> Category:
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist as exc:
            raise NotFoundException(f"Category '{slug}' not found") from exc


class TagRepository:
    """Singleton repository for Tag ORM queries."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "TagRepository":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_all(self) -> QuerySet:
        return Tag.objects.all().order_by("name")

    def get_or_create(self, name: str) -> Tag:
        tag_obj, _ = Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
        return tag_obj
