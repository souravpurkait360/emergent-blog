import logging

from rest_framework import permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.exceptions import BlogAPIException
from apps.posts.serializers.post_serializers import PostCreateSerializer, PostListSerializer
from apps.posts.services.post_service import PostService

logger = logging.getLogger(__name__)
PAGE_SIZE = 9


class PostListAPIView(APIView):
    """GET /api/posts/ – paginated feed. POST – create a new post."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request: Request) -> Response:
        post_service = PostService.get_instance()
        search_query = request.query_params.get("search", "")
        category_slug = request.query_params.get("category__slug", "")
        queryset = post_service.get_feed(user=request.user, search=search_query, category_slug=category_slug)

        page_number = int(request.query_params.get("page", 1))
        total_count = queryset.count()
        start = (page_number - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        posts = queryset[start:end]

        return Response({
            "count": total_count,
            "results": PostListSerializer(posts, many=True, context={"request": request}).data,
        })

    def post(self, request: Request) -> Response:
        try:
            post_service = PostService.get_instance()
            input_serializer = PostCreateSerializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)
            post = post_service.create_post(request.user, input_serializer.validated_data)
            return Response(
                PostListSerializer(post, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
        except Exception as exc:
            logger.exception("Post creation failed: %s", exc)
            return Response({"error": "Post creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
