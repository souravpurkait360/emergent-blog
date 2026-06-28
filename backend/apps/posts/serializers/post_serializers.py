import os

from rest_framework import serializers

from apps.accounts.serializers.user_serializer import UserSerializer
from apps.posts.models import Post
from apps.posts.serializers.category_tag_serializers import CategorySerializer, TagSerializer
from apps.posts.serializers.comment_serializer import CommentSerializer

BACKEND_URL = os.environ.get("FRONTEND_URL", "")


class PostListSerializer(serializers.ModelSerializer):
    """Output DTO for post listings – no full content, no comments."""

    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "ai_summary", "cover_image_url",
            "author", "category", "tags", "status", "views", "created_at", "comment_count",
        ]

    def get_comment_count(self, post_obj) -> int:
        return post_obj.comments.count()

    def get_cover_image_url(self, post_obj) -> str | None:
        if not post_obj.cover_image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(post_obj.cover_image.url)
        return f"{BACKEND_URL}{post_obj.cover_image.url}"


class PostDetailSerializer(PostListSerializer):
    """Output DTO for the post detail page – includes content and comments."""

    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ["content", "ai_summary", "comments", "updated_at"]


class PostCreateSerializer(serializers.Serializer):
    """Input DTO for post create / update operations."""

    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    status = serializers.ChoiceField(choices=["draft", "published"], default="draft")
    category_id = serializers.IntegerField(required=False, allow_null=True)
    tag_names = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    ai_summary = serializers.CharField(required=False, allow_blank=True, default="")
    cover_image = serializers.ImageField(required=False, allow_null=True)
