from django.urls import path

from apps.posts.api.v1.admin_post_delete_api import AdminPostDeleteAPIView
from apps.posts.api.v1.admin_post_list_api import AdminPostListAPIView
from apps.posts.api.v1.category_list_api import CategoryListAPIView
from apps.posts.api.v1.comment_create_api import CommentCreateAPIView
from apps.posts.api.v1.comment_delete_api import CommentDeleteAPIView
from apps.posts.api.v1.my_posts_api import MyPostsAPIView
from apps.posts.api.v1.post_detail_api import PostDetailAPIView
from apps.posts.api.v1.post_list_api import PostListAPIView
from apps.posts.api.v1.tag_list_api import TagListAPIView

# NOTE: specific paths must come before slug-based paths to avoid Django routing conflicts
urlpatterns = [
    path("posts/my/", MyPostsAPIView.as_view(), name="posts-mine"),
    path("posts/admin/", AdminPostListAPIView.as_view(), name="posts-admin-list"),
    path("posts/", PostListAPIView.as_view(), name="posts-list"),
    path("posts/<slug:slug>/", PostDetailAPIView.as_view(), name="posts-detail"),
    path("posts/<slug:slug>/comments/", CommentCreateAPIView.as_view(), name="comments-create"),
    path("comments/<int:pk>/", CommentDeleteAPIView.as_view(), name="comments-delete"),
    path("categories/", CategoryListAPIView.as_view(), name="categories-list"),
    path("tags/", TagListAPIView.as_view(), name="tags-list"),
    path("posts/admin/<int:pk>/", AdminPostDeleteAPIView.as_view(), name="posts-admin-delete"),
]
