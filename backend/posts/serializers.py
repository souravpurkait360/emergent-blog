import os
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Tag, Post, Comment

User = get_user_model()
BACKEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:8001')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count']

    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'ai_summary', 'cover_image_url', 'author',
                  'category', 'tags', 'status', 'views', 'created_at', 'comment_count']

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return f"{BACKEND_URL}/api/media/{obj.cover_image}"
        return None


class PostDetailSerializer(PostListSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['content', 'ai_summary', 'comments', 'updated_at']


class PostCreateSerializer(serializers.ModelSerializer):
    tag_names = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'cover_image', 'category_id', 'tag_names', 'status', 'ai_summary']

    def _handle_tags(self, post, tag_names):
        tags = []
        for name in tag_names:
            name = name.strip()
            if name:
                tag, _ = Tag.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
                tags.append(tag)
        post.tags.set(tags)

    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        category_id = validated_data.pop('category_id', None)
        if category_id:
            try:
                validated_data['category'] = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                pass
        post = Post.objects.create(**validated_data)
        self._handle_tags(post, tag_names)
        return post

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', None)
        category_id = validated_data.pop('category_id', None)
        if category_id is not None:
            try:
                validated_data['category'] = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                validated_data['category'] = None
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if tag_names is not None:
            self._handle_tags(instance, tag_names)
        return instance


def slugify(name):
    from django.utils.text import slugify as dj_slugify
    return dj_slugify(name)
