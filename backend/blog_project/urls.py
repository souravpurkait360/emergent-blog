from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.posts.urls")),
    path("api/ai/", include("apps.ai.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
