from django.urls import path
from .views import (CategoryListView, TagListView, PostListView, PostDetailView,
                    MyPostsView, CommentCreateView, CommentDeleteView,
                    AdminPostListView, AdminPostDeleteView)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/my/', MyPostsView.as_view(), name='my-posts'),
    path('posts/admin/', AdminPostListView.as_view(), name='admin-posts'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/comments/', CommentCreateView.as_view(), name='add-comment'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='delete-comment'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('posts/admin/<int:pk>/', AdminPostDeleteView.as_view(), name='admin-post-delete'),
]
