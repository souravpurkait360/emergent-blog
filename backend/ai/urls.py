from django.urls import path
from .views import AIAssistView, AISummarizeView

urlpatterns = [
    path('assist/', AIAssistView.as_view(), name='ai-assist'),
    path('summarize/', AISummarizeView.as_view(), name='ai-summarize'),
]
