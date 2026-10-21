from django.contrib import admin
from django.urls import path, re_path, include
from server.config.auth_views import RegisterView, LoginView, LogoutView, CurrentUserView
from server.config.static_views import (
    serve_about,
    serve_contact,
    serve_static_css,
    serve_frontend_asset,
    serve_frontend_app,
)
from server.dealerships.views import DealerListView, DealerDetailView, CarMakeListView
from server.reviews.views import DealerReviewsView
from server.sentiment.views import FetchSentimentView

urlpatterns = [
    # Admin Interface
    path("admin/", admin.site.urls),

    # Authentication API
    path("api/auth/register/", RegisterView.as_view(), name="auth-register"),
    path("api/auth/login/", LoginView.as_view(), name="auth-login"),
    path("api/auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("api/auth/me/", CurrentUserView.as_view(), name="auth-me"),

    # Dealerships, Reviews, Sentiment APIs
    path("api/", include("server.dealerships.urls")),
    path("api/", include("server.reviews.urls")),
    path("api/", include("server.sentiment.urls")),

    # Coursera / Express Capstone Microservice Routing Standards
    path("fetchDealers", DealerListView.as_view(), name="fetch-dealers"),
    path("fetchDealers/", DealerListView.as_view(), name="fetch-dealers-slash"),
    path("fetchDealers/<str:state>", DealerListView.as_view(), name="fetch-dealers-state"),
    path("fetchDealers/<str:state>/", DealerListView.as_view(), name="fetch-dealers-state-slash"),
    path("fetchDealer/<int:dealer_id>", DealerDetailView.as_view(), name="fetch-dealer"),
    path("fetchDealer/<int:dealer_id>/", DealerDetailView.as_view(), name="fetch-dealer-slash"),
    path("fetchReviews/dealer/<int:dealer_id>", DealerReviewsView.as_view(), name="fetch-dealer-reviews"),
    path("fetchReviews/dealer/<int:dealer_id>/", DealerReviewsView.as_view(), name="fetch-dealer-reviews-slash"),
    path("fetchSentiment/<path:text>", FetchSentimentView.as_view(), name="fetch-sentiment"),
    path("fetchSentiment/<path:text>/", FetchSentimentView.as_view(), name="fetch-sentiment-slash"),
    path("fetchCars", CarMakeListView.as_view(), name="fetch-cars"),
    path("fetchCars/", CarMakeListView.as_view(), name="fetch-cars-slash"),

    # Static HTML Deliverables
    path("about/", serve_about, name="about-page"),
    path("about.html", serve_about, name="about-html-page"),
    path("contact/", serve_contact, name="contact-page"),
    path("contact.html", serve_contact, name="contact-html-page"),
    path("style.css", serve_static_css, name="static-style-css"),

    # Built React Assets
    re_path(r"^assets/(?P<path>.*)$", serve_frontend_asset, name="frontend-asset"),

    # Capstone Compatibility Aliases
    path("djangoapp/login", LoginView.as_view(), name="alias-login"),
    path("djangoapp/logout", LogoutView.as_view(), name="alias-logout"),
    path("djangoapp/register", RegisterView.as_view(), name="alias-register"),
    path("djangoapp/get_dealers", DealerListView.as_view(), name="alias-dealers"),
    path("djangoapp/get_dealers/", DealerListView.as_view(), name="alias-dealers-slash"),
    path("djangoapp/get_dealers/<str:state>", DealerListView.as_view(), name="alias-dealers-state"),
    path("djangoapp/get_dealers/<str:state>/", DealerListView.as_view(), name="alias-dealers-state-slash"),
    path("djangoapp/dealer/<int:dealer_id>", DealerDetailView.as_view(), name="alias-dealer-detail"),
    path("djangoapp/dealer/<int:dealer_id>/", DealerDetailView.as_view(), name="alias-dealer-detail-slash"),
    path("djangoapp/get_cars", CarMakeListView.as_view(), name="alias-cars"),
    path("djangoapp/get_cars/", CarMakeListView.as_view(), name="alias-cars-slash"),
    path("djangoapp/reviews/dealer/<int:dealer_id>", DealerReviewsView.as_view(), name="alias-dealer-reviews"),
    path("djangoapp/reviews/dealer/<int:dealer_id>/", DealerReviewsView.as_view(), name="alias-dealer-reviews-slash"),
    path("djangoapp/add_review", DealerReviewsView.as_view(), name="alias-add-review"),
    path("djangoapp/add_review/", DealerReviewsView.as_view(), name="alias-add-review-slash"),
    path("djangoapp/analyze/<path:text>", FetchSentimentView.as_view(), name="djangoapp-analyze"),

    # Frontend Single Page Application Root & Routes
    path("", serve_frontend_app, name="frontend-root"),
    re_path(r"^(?:login|register|dealers|dealer/.*)/?$", serve_frontend_app, name="frontend-spa-routes"),
]
