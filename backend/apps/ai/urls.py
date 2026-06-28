from django.urls import path

from apps.ai.api.v1.assist_api import AIAssistAPIView
from apps.ai.api.v1.summarize_api import AISummarizeAPIView

urlpatterns = [
    path("assist/", AIAssistAPIView.as_view(), name="ai-assist"),
    path("summarize/", AISummarizeAPIView.as_view(), name="ai-summarize"),
]
