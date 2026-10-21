from django.db import models


class CarMake(models.Model):
    """Represents a car manufacturer/make."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True, default="USA")

    class Meta:
        ordering = ["name"]
        verbose_name = "Car Make"
        verbose_name_plural = "Car Makes"

    def __str__(self):
        return self.name


class Dealer(models.Model):
    """Represents a dealership branch."""
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, db_index=True)
    st = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=20)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)
    phone = models.CharField(max_length=50, blank=True, default="1-800-555-CARS")
    email = models.EmailField(blank=True, default="info@dealerships.example.com")
    website = models.URLField(blank=True, default="https://dealerships.example.com")
    image = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Dealership"
        verbose_name_plural = "Dealerships"

    def __str__(self):
        return f"{self.full_name} ({self.city}, {self.state})"


class CarModel(models.Model):
    """Represents a car model produced by a CarMake."""
    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("HATCHBACK", "Hatchback"),
        ("TRUCK", "Truck"),
        ("COUPE", "Coupe"),
        ("VAN", "Van"),
        ("ELECTRIC", "Electric"),
    ]

    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="models"
    )
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="car_models"
    )
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=50, choices=CAR_TYPES, default="SEDAN")
    year = models.IntegerField(default=2024)

    class Meta:
        ordering = ["car_make__name", "name", "-year"]
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
