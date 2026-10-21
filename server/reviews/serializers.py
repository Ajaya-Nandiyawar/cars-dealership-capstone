from rest_framework import serializers
from .models import Review
from server.dealerships.models import Dealer


class ReviewSerializer(serializers.ModelSerializer):
    dealer_id = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(),
        source="dealer",
        write_only=True,
        required=False
    )
    dealer_name = serializers.CharField(source="dealer.full_name", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "dealer",
            "dealer_id",
            "dealer_name",
            "user",
            "name",
            "review",
            "purchase",
            "purchase_date",
            "car_make",
            "car_model",
            "car_year",
            "sentiment",
            "sentiment_score",
            "created_at",
        ]
        read_only_fields = ["id", "dealer", "user", "sentiment", "sentiment_score", "created_at"]
