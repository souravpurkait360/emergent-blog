from rest_framework import serializers

from apps.posts.models import Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """Output DTO for category with published post count."""

    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "post_count"]

    def get_post_count(self, category_obj) -> int:
        return category_obj.posts.filter(status="published").count()


class TagSerializer(serializers.ModelSerializer):
    """Output DTO for a tag."""

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
