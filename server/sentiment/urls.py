from django.urls import path
from .views import SentimentAnalysisView

urlpatterns = [
    path("analyze-review/", SentimentAnalysisView.as_view(), name="analyze-review"),
]
