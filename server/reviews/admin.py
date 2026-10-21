from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dealer",
        "name",
        "purchase",
        "car_make",
        "car_model",
        "sentiment",
        "sentiment_score",
        "created_at",
    )
    list_filter = ("sentiment", "purchase", "dealer__state", "created_at")
    search_fields = ("name", "review", "dealer__full_name", "car_make", "car_model")
