from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from server.dealerships.models import Dealer
from server.sentiment.services import analyze_text_sentiment
from .models import Review
from .serializers import ReviewSerializer


class DealerReviewsView(APIView):
    """
    GET /api/dealers/<dealer_id>/reviews/
    POST /api/dealers/<dealer_id>/reviews/
    """

    def get(self, request, dealer_id):
        # Validate that the dealer exists
        dealer = get_object_or_404(Dealer, pk=dealer_id)
        reviews = Review.objects.filter(dealer=dealer).order_by("-created_at")
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, dealer_id):
        # Only authenticated users can submit reviews
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required. Please log in to post a review."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Validate dealer
        dealer = get_object_or_404(Dealer, pk=dealer_id)

        data = request.data
        review_text = data.get("review")

        if not review_text or not str(review_text).strip():
            return Response(
                {"error": "Review text is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Reviewer name defaults to user full name or username
        reviewer_name = (
            data.get("name")
            or request.user.get_full_name()
            or request.user.username
        ).strip()

        # Perform sentiment analysis
        sentiment_result = analyze_text_sentiment(str(review_text))
        sentiment = sentiment_result.get("sentiment", "neutral")
        sentiment_score = sentiment_result.get("score", 0.0)

        # Optional fields
        purchase = bool(data.get("purchase", False))
        purchase_date = data.get("purchase_date") or None
        car_make = data.get("car_make", "")
        car_model = data.get("car_model", "")
        car_year = data.get("car_year") or None

        review = Review.objects.create(
            dealer=dealer,
            user=request.user,
            name=reviewer_name,
            review=review_text.strip(),
            purchase=purchase,
            purchase_date=purchase_date,
            car_make=car_make,
            car_model=car_model,
            car_year=car_year,
            sentiment=sentiment,
            sentiment_score=sentiment_score,
        )

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DealerReviewsAliasView(DealerReviewsView):
    """Alias for /api/reviews/dealer/<dealer_id>/"""
    pass
