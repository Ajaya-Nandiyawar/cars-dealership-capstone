from django.urls import path
from .views import DealerListView, DealerDetailView, DealerByStateView, CarMakeListView

urlpatterns = [
    path("dealers/", DealerListView.as_view(), name="dealer-list"),
    path("dealers/<int:dealer_id>/", DealerDetailView.as_view(), name="dealer-detail"),
    path("dealers/state/<str:state>/", DealerByStateView.as_view(), name="dealer-by-state"),
    path("car-makes/", CarMakeListView.as_view(), name="car-make-list"),
]
