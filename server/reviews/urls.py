from django.urls import path
from .views import DealerReviewsView, DealerReviewsAliasView

urlpatterns = [
    path("dealers/<int:dealer_id>/reviews/", DealerReviewsView.as_view(), name="dealer-reviews"),
    path("reviews/dealer/<int:dealer_id>/", DealerReviewsAliasView.as_view(), name="dealer-reviews-alias"),
]
