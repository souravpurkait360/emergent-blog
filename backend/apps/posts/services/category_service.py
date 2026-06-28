from apps.core.exceptions import ValidationException
from apps.posts.models import Category
from apps.posts.repositories.category_tag_repository import CategoryRepository, TagRepository


class CategoryService:
    """Singleton service for category business logic."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "CategoryService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self._category_repository = CategoryRepository.get_instance()

    def get_all(self):
        return self._category_repository.get_all()

    def create_category(self, name: str, description: str = "") -> Category:
        name = name.strip()
        if not name:
            raise ValidationException("Category name cannot be empty")
        return self._category_repository.create(name=name, description=description)


class TagService:
    """Singleton service for tag business logic."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "TagService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self._tag_repository = TagRepository.get_instance()

    def get_all(self):
        return self._tag_repository.get_all()
