from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Tag, Post, Comment
from .serializers import (CategorySerializer, TagSerializer, PostListSerializer,
                           PostDetailSerializer, PostCreateSerializer, CommentSerializer)


class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        author = getattr(obj, 'author', None)
        return (author == request.user) or (request.user.role == 'admin')


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class PostListView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'tags__slug', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments')
        user = self.request.user
        if user.is_authenticated:
            return qs.filter(Q(status='published') | Q(author=user))
        return qs.filter(status='published')

    def get_serializer_class(self):
        return PostCreateSerializer if self.request.method == 'POST' else PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response(PostListSerializer(post).data, status=status.HTTP_201_CREATED)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'slug'
    permission_classes = [IsAuthorOrAdmin]

    def get_queryset(self):
        return Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments__author')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateSerializer
        return PostDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        instance.refresh_from_db()
        return Response(PostDetailSerializer(instance).data)


class MyPostsView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = Post.objects.get(slug=self.kwargs['slug'])
        serializer.save(author=self.request.user, post=post)


class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Comment.objects.all()
        return Comment.objects.filter(author=self.request.user)


class AdminPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all().select_related('author', 'category').order_by('-created_at')


class AdminPostDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
