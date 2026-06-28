from rest_framework import serializers

from apps.posts.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Output DTO for comments, includes author details."""

    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at"]

    def get_author(self, comment_obj) -> dict:
        return {
            "id": comment_obj.author.id,
            "email": comment_obj.author.email,
            "username": comment_obj.author.username,
            "first_name": comment_obj.author.first_name,
            "last_name": comment_obj.author.last_name,
        }
