from rest_framework import serializers
from .models import CarMake, Dealer, CarModel


class CarModelSerializer(serializers.ModelSerializer):
    car_make_name = serializers.CharField(source="car_make.name", read_only=True)

    class Meta:
        model = CarModel
        fields = [
            "id",
            "name",
            "car_make",
            "car_make_name",
            "car_type",
            "year",
            "dealer",
        ]


class CarMakeSerializer(serializers.ModelSerializer):
    models = CarModelSerializer(many=True, read_only=True)

    class Meta:
        model = CarMake
        fields = [
            "id",
            "name",
            "description",
            "country",
            "models",
        ]


class DealerSerializer(serializers.ModelSerializer):
    car_models = CarModelSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source="reviews.count", read_only=True)

    class Meta:
        model = Dealer
        fields = [
            "id",
            "full_name",
            "short_name",
            "city",
            "state",
            "st",
            "address",
            "zip",
            "lat",
            "long",
            "phone",
            "email",
            "website",
            "image",
            "car_models",
            "reviews_count",
        ]
