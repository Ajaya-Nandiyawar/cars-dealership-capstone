from django.db import models
from django.contrib.auth.models import User
from server.dealerships.models import Dealer


class Review(models.Model):
    """Represents a customer review for a dealership."""
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_reviews"
    )
    name = models.CharField(max_length=100, default="Anonymous")
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=50, default="neutral")
    sentiment_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Dealer Review"
        verbose_name_plural = "Dealer Reviews"

    def __str__(self):
        return f"Review #{self.id} for {self.dealer.full_name} by {self.name} ({self.sentiment})"
